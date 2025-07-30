# Django Football Club Website - VPS Deployment Guide

This guide provides step-by-step instructions for deploying the TJ Družba Hlavnice Django website on an Ubuntu VPS with a custom domain.

## Table of Contents

1. [VPS Server Preparation](#vps-server-preparation)
2. [Domain Configuration](#domain-configuration)
3. [Server Setup](#server-setup)
4. [Application Deployment](#application-deployment)
5. [Web Server Configuration](#web-server-configuration)
6. [SSL Certificate Setup](#ssl-certificate-setup)
7. [Database Configuration](#database-configuration)
8. [Static Files & Media](#static-files--media)
9. [Process Management](#process-management)
10. [Monitoring & Maintenance](#monitoring--maintenance)
11. [Troubleshooting](#troubleshooting)

## VPS Server Preparation

### Minimum Requirements

- **RAM**: 1GB minimum (2GB recommended)
- **Storage**: 20GB minimum (40GB recommended)
- **CPU**: 1 core minimum (2 cores recommended)
- **OS**: Ubuntu 20.04 LTS or 22.04 LTS

### Initial Server Access

```bash
# Connect to your VPS via SSH
ssh root@your-server-ip

# Or if you have a non-root user
ssh username@your-server-ip
```

## Domain Configuration

### 1. DNS Records Setup

Configure the following DNS records with your domain provider:

```
Type    Name    Value               TTL
A       @       your-server-ip      3600
A       www     your-server-ip      3600
CNAME   *       yourdomain.com      3600
```

### 2. Verify DNS Propagation

```bash
# Check if DNS is propagated
dig yourdomain.com
dig www.yourdomain.com
```

## Server Setup

### 1. Update System

```bash
# Update package lists and upgrade system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git vim htop unzip software-properties-common
```

### 2. Create Application User

```bash
# Create a user for the application
sudo adduser tjhlavnice
sudo usermod -aG sudo tjhlavnice

# Switch to the new user
su - tjhlavnice
```

### 3. Install Python and Dependencies

```bash
# Install Python 3.11 and pip
sudo apt install -y python3.11 python3.11-venv python3-pip python3.11-dev

# Install system dependencies
sudo apt install -y build-essential libpq-dev nginx supervisor
```

### 4. Install PostgreSQL

```bash
# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql

-- In PostgreSQL shell:
CREATE DATABASE tjhlavnice;
CREATE USER tjhlavnice WITH ENCRYPTED PASSWORD 'your-strong-password';
GRANT ALL PRIVILEGES ON DATABASE tjhlavnice TO tjhlavnice;
ALTER USER tjhlavnice CREATEDB;
\q
```

## Application Deployment

### 1. Clone Repository

```bash
# Navigate to home directory
cd /home/tjhlavnice

# Clone your repository
git clone https://github.com/yourusername/tjhlavnice.git
cd tjhlavnice

# Or upload files via SCP if not using Git
# scp -r /path/to/local/project tjhlavnice@your-server-ip:/home/tjhlavnice/
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### 3. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# If requirements.txt doesn't exist, install manually:
pip install django==5.2.4
pip install psycopg2-binary
pip install gunicorn
pip install pillow
pip install python-decouple
```

### 4. Environment Configuration

```bash
# Create environment file
nano .env
```

Add the following content to `.env`:

```env
# Django Settings
SECRET_KEY=your-very-long-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip

# Database Configuration
DB_NAME=tjhlavnice
DB_USER=tjhlavnice
DB_PASSWORD=your-strong-password
DB_HOST=localhost
DB_PORT=5432

# Static and Media Files
STATIC_URL=/static/
STATIC_ROOT=/home/tjhlavnice/tjhlavnice/staticfiles/
MEDIA_URL=/media/
MEDIA_ROOT=/home/tjhlavnice/tjhlavnice/media/

# Email Configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 5. Django Configuration

```bash
# Update settings.py for production
nano tjhlavnice/settings.py
```

Update `settings.py`:

```python
import os
from decouple import config

# Production settings
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Static files
STATIC_URL = config('STATIC_URL', default='/static/')
STATIC_ROOT = config('STATIC_ROOT', default=os.path.join(BASE_DIR, 'staticfiles'))

# Media files
MEDIA_URL = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = config('MEDIA_ROOT', default=os.path.join(BASE_DIR, 'media'))

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### 6. Run Django Setup

```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Test the application
python manage.py runserver 0.0.0.0:8000
```

## Web Server Configuration

### 1. Gunicorn Configuration

```bash
# Create Gunicorn configuration
nano /home/tjhlavnice/tjhlavnice/gunicorn.conf.py
```

Add Gunicorn configuration:

```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 5
preload_app = True
user = "tjhlavnice"
group = "tjhlavnice"
```

### 2. Create Gunicorn Service

```bash
# Create systemd service file
sudo nano /etc/systemd/system/tjhlavnice.service
```

Add service configuration:

```ini
[Unit]
Description=TJ Hlavnice Django Application
After=network.target

[Service]
User=tjhlavnice
Group=tjhlavnice
WorkingDirectory=/home/tjhlavnice/tjhlavnice
Environment="PATH=/home/tjhlavnice/tjhlavnice/venv/bin"
ExecStart=/home/tjhlavnice/tjhlavnice/venv/bin/gunicorn --config gunicorn.conf.py tjhlavnice.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Start Gunicorn Service

```bash
# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl start tjhlavnice
sudo systemctl enable tjhlavnice

# Check status
sudo systemctl status tjhlavnice
```

### 4. Nginx Configuration

```bash
# Create Nginx site configuration
sudo nano /etc/nginx/sites-available/tjhlavnice
```

Add Nginx configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 100M;

    # Static files
    location /static/ {
        alias /home/tjhlavnice/tjhlavnice/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /home/tjhlavnice/tjhlavnice/media/;
        expires 30d;
        add_header Cache-Control "public";
    }

    # Main application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### 5. Enable Nginx Site

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/tjhlavnice /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

## SSL Certificate Setup

### 1. Install Certbot

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

### 2. Update Nginx for HTTPS

After Certbot, your Nginx config will be automatically updated. Verify the configuration:

```bash
# Check updated configuration
sudo nano /etc/nginx/sites-available/tjhlavnice

# Restart Nginx
sudo systemctl restart nginx
```

## Database Configuration

### 1. PostgreSQL Optimization

```bash
# Edit PostgreSQL configuration
sudo nano /etc/postgresql/14/main/postgresql.conf
```

Optimize for your server:

```conf
# Memory settings
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB

# Connection settings
max_connections = 100
```

### 2. Database Backup Script

```bash
# Create backup directory
mkdir -p /home/tjhlavnice/backups

# Create backup script
nano /home/tjhlavnice/backup_db.sh
```

Add backup script:

```bash
#!/bin/bash
BACKUP_DIR="/home/tjhlavnice/backups"
DB_NAME="tjhlavnice"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup
pg_dump $DB_NAME > $BACKUP_DIR/tjhlavnice_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "tjhlavnice_*.sql" -mtime +7 -delete

echo "Backup completed: tjhlavnice_$DATE.sql"
```

```bash
# Make script executable
chmod +x /home/tjhlavnice/backup_db.sh

# Add to crontab for daily backups
crontab -e

# Add this line for daily backup at 2 AM
0 2 * * * /home/tjhlavnice/backup_db.sh
```

## Static Files & Media

### 1. Create Media Directory

```bash
# Create media directory with proper permissions
mkdir -p /home/tjhlavnice/tjhlavnice/media
sudo chown -R tjhlavnice:tjhlavnice /home/tjhlavnice/tjhlavnice/media
sudo chmod -R 755 /home/tjhlavnice/tjhlavnice/media
```

### 2. Static Files Optimization

```bash
# Ensure static files are collected
cd /home/tjhlavnice/tjhlavnice
source venv/bin/activate
python manage.py collectstatic --noinput

# Set proper permissions
sudo chown -R tjhlavnice:tjhlavnice /home/tjhlavnice/tjhlavnice/staticfiles
sudo chmod -R 755 /home/tjhlavnice/tjhlavnice/staticfiles
```

## Process Management

### 1. Supervisor Configuration (Alternative to systemd)

```bash
# Install Supervisor
sudo apt install supervisor

# Create Supervisor configuration
sudo nano /etc/supervisor/conf.d/tjhlavnice.conf
```

Add Supervisor configuration:

```ini
[program:tjhlavnice]
command=/home/tjhlavnice/tjhlavnice/venv/bin/gunicorn --config gunicorn.conf.py tjhlavnice.wsgi:application
directory=/home/tjhlavnice/tjhlavnice
user=tjhlavnice
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/tjhlavnice.log
```

```bash
# Update Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start tjhlavnice
```

## Monitoring & Maintenance

### 1. Log Management

```bash
# Create log rotation configuration
sudo nano /etc/logrotate.d/tjhlavnice
```

Add log rotation:

```
/var/log/supervisor/tjhlavnice.log {
    daily
    missingok
    rotate 30
    compress
    notifempty
    create 644 tjhlavnice tjhlavnice
    postrotate
        supervisorctl restart tjhlavnice
    endscript
}
```

### 2. System Monitoring Script

```bash
# Create monitoring script
nano /home/tjhlavnice/monitor.sh
```

Add monitoring script:

```bash
#!/bin/bash

# Check if Gunicorn is running
if ! pgrep -f "gunicorn.*tjhlavnice" > /dev/null; then
    echo "$(date): Gunicorn not running, restarting..." >> /home/tjhlavnice/monitor.log
    sudo systemctl restart tjhlavnice
fi

# Check if Nginx is running
if ! pgrep nginx > /dev/null; then
    echo "$(date): Nginx not running, restarting..." >> /home/tjhlavnice/monitor.log
    sudo systemctl restart nginx
fi

# Check disk space
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "$(date): Disk usage is ${DISK_USAGE}%" >> /home/tjhlavnice/monitor.log
fi
```

```bash
# Make executable and add to crontab
chmod +x /home/tjhlavnice/monitor.sh

# Add to crontab (every 5 minutes)
crontab -e

# Add this line
*/5 * * * * /home/tjhlavnice/monitor.sh
```

### 3. Update Script

```bash
# Create update script
nano /home/tjhlavnice/update.sh
```

Add update script:

```bash
#!/bin/bash
cd /home/tjhlavnice/tjhlavnice

# Backup database
./backup_db.sh

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install new dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Restart application
sudo systemctl restart tjhlavnice

echo "Update completed successfully!"
```

```bash
# Make executable
chmod +x /home/tjhlavnice/update.sh
```

## Troubleshooting

### 1. Common Issues

#### Application Won't Start

```bash
# Check Gunicorn logs
sudo journalctl -u tjhlavnice -f

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log

# Check if port is in use
sudo netstat -tlnp | grep :8000
```

#### Static Files Not Loading

```bash
# Check static files directory
ls -la /home/tjhlavnice/tjhlavnice/staticfiles/

# Recollect static files
cd /home/tjhlavnice/tjhlavnice
source venv/bin/activate
python manage.py collectstatic --noinput

# Check Nginx configuration
sudo nginx -t
```

#### Database Connection Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test database connection
sudo -u postgres psql -c "SELECT version();"

# Check Django database connection
cd /home/tjhlavnice/tjhlavnice
source venv/bin/activate
python manage.py dbshell
```

### 2. Performance Optimization

#### Enable Gzip Compression

Add to Nginx configuration:

```nginx
# Add inside server block
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
```

#### Cache Static Files

Add to Nginx configuration:

```nginx
# Add inside server block
location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}
```

### 3. Security Hardening

#### Firewall Configuration

```bash
# Install and configure UFW
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
```

#### Fail2ban Setup

```bash
# Install Fail2ban
sudo apt install fail2ban

# Create jail configuration
sudo nano /etc/fail2ban/jail.local
```

Add Fail2ban configuration:

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[nginx-http-auth]
enabled = true

[nginx-limit-req]
enabled = true
```

```bash
# Restart Fail2ban
sudo systemctl restart fail2ban
```

## Final Verification

### 1. Test Your Website

- Visit `https://yourdomain.com`
- Check all pages load correctly
- Test admin panel at `https://yourdomain.com/admin/`
- Verify SSL certificate is working
- Test responsive design on mobile

### 2. Performance Testing

```bash
# Install and use tools for testing
sudo apt install apache2-utils

# Test concurrent connections
ab -n 100 -c 10 https://yourdomain.com/
```

### 3. SEO and Analytics

Consider adding:

- Google Analytics
- Google Search Console
- robots.txt file
- sitemap.xml

Your Django football club website should now be fully deployed and accessible at your custom domain with SSL encryption!

## Support

For issues specific to this deployment:

1. Check the troubleshooting section above
2. Review log files in `/var/log/`
3. Verify all services are running: `sudo systemctl status nginx tjhlavnice postgresql`

Remember to keep your system updated and monitor your application regularly for optimal performance and security.
