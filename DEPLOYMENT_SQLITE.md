# VPS Deployment Guide (Own Domain + SQLite)

This guide describes a minimal, production-ready deployment of this Django project on an Ubuntu VPS using your own domain and the built-in SQLite database.

It assumes a clean server, Nginx as reverse proxy, Gunicorn for the WSGI server, and free HTTPS with Certbot.

---

## 0) Project snapshot (what you have)

- Framework: Django 5.2.4
- App: `football`
- DB: SQLite (file `db.sqlite3` located in project root)
- Static config:
  - `STATIC_URL = 'static/'` (recommend: change to `/static/` in production)
  - `STATIC_ROOT = <project>/staticfiles`
  - Additional static in `<project>/static`
- Media config:
  - `MEDIA_URL = '/media/'`
  - `MEDIA_ROOT = <project>/media`
- Admin/media tools: `django-ckeditor`

---

## 1) Prerequisites

- Ubuntu 20.04/22.04 LTS VPS
- A domain, e.g. `example.com`, pointed to the server IP (A records for `example.com` and `www.example.com`).
- A non-root user with sudo (shown here as `deploy` but you can use another name).

### Install system packages
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip nginx git
# For HTTPS later
sudo apt install -y certbot python3-certbot-nginx
```

---

## 2) Create user and directories
```bash
# Create a deployment user (skip if you already have one)
sudo adduser deploy
sudo usermod -aG sudo deploy

# Switch to the user
su - deploy

# Create project directory
mkdir -p ~/apps && cd ~/apps
```

---

## 3) Get the code on the server
```bash
# If using Git
git clone https://github.com/<your-account>/tjhlavnice.git
cd tjhlavnice

# Or upload the project via scp/rsync and then cd into it
```

The project root should contain: `manage.py`, `requirements.txt`, `tjhlavnice/`, `football/`, `templates/`, `static/`, `media/`, `db.sqlite3`, etc.

---

## 4) Python virtual environment + dependencies
```bash
# Create and activate venv
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Install a production WSGI server
pip install gunicorn
```

Optional: Save Gunicorn to requirements for future installs:
```bash
echo 'gunicorn' >> requirements.txt
```

---

## 5) Configure Django for production

Open `tjhlavnice/settings.py` and apply/verify these changes:

- Set your domain and disable debug:
```python
DEBUG = False
ALLOWED_HOSTS = [
    'example.com',
    'www.example.com',
]
```

- Add CSRF trusted origins (Django 4+/5+):
```python
CSRF_TRUSTED_ORIGINS = [
    'https://example.com',
    'https://www.example.com',
]
```

- Ensure static URL is absolute (recommended in production):
```python
STATIC_URL = '/static/'  # instead of 'static/'
```

- Keep SQLite as-is:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

- Optional security hardening for HTTPS:
```python
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

Notes:
- SQLite file `db.sqlite3` must be writable by the system user running the app (we use user `deploy`).
- Consider restricting CORS in production (current project enables `CORS_ALLOW_ALL_ORIGINS = True`).

---

## 6) Django setup
```bash
# From project root
source venv/bin/activate

# Apply migrations
python manage.py migrate

# Collect static
python manage.py collectstatic --noinput

# Create a superuser (if needed)
python manage.py createsuperuser
```

Set permissions so the app user owns the project and the SQLite database:
```bash
cd ~/apps/tjhlavnice
chown -R deploy:deploy .
chmod 664 db.sqlite3 || true
# Make sure the directory is writable by the owner
chmod 775 .
```

---

## 7) Run Gunicorn with systemd

Create a systemd service file:
```bash
sudo tee /etc/systemd/system/tjhlavnice.service > /dev/null << 'EOF'
[Unit]
Description=TJ Hlavnice Django (Gunicorn)
After=network.target

[Service]
User=deploy
Group=www-data
WorkingDirectory=/home/deploy/apps/tjhlavnice
Environment="PATH=/home/deploy/apps/tjhlavnice/venv/bin"
ExecStart=/home/deploy/apps/tjhlavnice/venv/bin/gunicorn \
  --workers 3 \
  --bind 127.0.0.1:8000 \
  tjhlavnice.wsgi:application
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

Start and enable the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start tjhlavnice
sudo systemctl enable tjhlavnice
sudo systemctl status tjhlavnice --no-pager
```

---

## 8) Nginx reverse proxy for your domain

Create an Nginx site config:
```bash
sudo tee /etc/nginx/sites-available/tjhlavnice > /dev/null << 'EOF'
server {
    listen 80;
    server_name example.com www.example.com;

    client_max_body_size 100M;

    # Static
    location /static/ {
        alias /home/tjhlavnice/apps/tjhlavnice/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media (uploads, CKEditor)
    location /media/ {
        alias /home/deploy/apps/tjhlavnice/media/;
        expires 30d;
        add_header Cache-Control "public";
    }

    # Django app
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
EOF
```

Enable and reload Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/tjhlavnice /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

Visit: `http://example.com`

---

## 9) Enable HTTPS (Let’s Encrypt)
```bash
sudo certbot --nginx -d example.com -d www.example.com
# Follow the prompts; Certbot will update Nginx automatically.

# Test renewal
sudo certbot renew --dry-run
```

After HTTPS, ensure Django security settings (see step 5) are set, especially `CSRF_TRUSTED_ORIGINS` and the cookie security flags.

---

## 10) Routine operations

### Deploying updates
```bash
cd /home/deploy/apps/tjhlavnice
source venv/bin/activate

git pull origin main  # or your branch
pip install -r requirements.txt --upgrade
python manage.py collectstatic --noinput
python manage.py migrate

sudo systemctl restart tjhlavnice
```

### Backups (SQLite + media)
```bash
cd /home/deploy/apps/tjhlavnice
# Simple timestamped backup of DB and media
TS=$(date +%Y%m%d_%H%M%S)
cp db.sqlite3 ~/backup_db_$TS.sqlite3
rsync -a media/ ~/backup_media_$TS/
```

### Logs and troubleshooting
```bash
# App (Gunicorn)
sudo journalctl -u tjhlavnice -f --no-pager

# Nginx
sudo tail -f /var/log/nginx/error.log

# Service status
sudo systemctl status tjhlavnice --no-pager
sudo systemctl status nginx --no-pager
```

- If you see SQLite "database is locked" or permission errors, ensure `db.sqlite3` and the project directory are owned by the running user and writable.
- If static files don’t load, re-run `collectstatic` and verify the Nginx `alias` paths.
- If CSRF errors occur after enabling HTTPS, verify `CSRF_TRUSTED_ORIGINS` includes your `https://` domains.

---

## 11) Optional hardening
- Use a firewall (UFW):
```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```
- Create a dedicated system user and directory just for the app (already done with `deploy`).
- Restrict CORS in production (avoid `CORS_ALLOW_ALL_ORIGINS = True`).

---

## 12) Quick checklist
- DNS A records point to server
- `DEBUG=False`, `ALLOWED_HOSTS` set, `CSRF_TRUSTED_ORIGINS` set
- `STATIC_URL='/static/'`, `STATIC_ROOT` exists and `collectstatic` run
- Gunicorn service running on `127.0.0.1:8000`
- Nginx reverse proxy configured for domain
- HTTPS enabled with Certbot
- SQLite file owned by the app user and writable

You are now running the site on your own domain with SQLite.
