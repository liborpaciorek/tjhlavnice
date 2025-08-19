# Troubleshooting 500 Errors - News and Gallery Pages

## Common Causes and Solutions

### 1. Missing Media Files
**Problem**: Production server can't find uploaded images
**Solution**: Ensure media files are uploaded to production server and permissions are correct

```bash
# On production server, check media directory
ls -la media/
ls -la media/news/
ls -la media/gallery/

# Fix permissions if needed
chmod -R 755 media/
```

### 2. Static Files Not Collected
**Problem**: CKEditor static files missing
**Solution**: Run collectstatic command

```bash
python manage.py collectstatic --noinput
```

### 3. Missing Dependencies
**Problem**: PIL/Pillow or other packages not installed
**Solution**: Install all requirements

```bash
pip install -r requirements.txt
```

### 4. Database Issues
**Problem**: Database not migrated or corrupted
**Solution**: Run migrations and check database

```bash
python manage.py migrate
python manage.py shell -c "from football.models import News, Gallery; print(f'News: {News.objects.count()}, Gallery: {Gallery.objects.count()}')"
```

### 5. Web Server Configuration
**Problem**: Apache/Nginx not configured to serve media files
**Solution**: Configure web server to serve /media/ and /static/

#### For Apache (.htaccess or virtual host):
```apache
Alias /media/ /path/to/your/project/media/
Alias /static/ /path/to/your/project/staticfiles/

<Directory /path/to/your/project/media>
    Require all granted
</Directory>

<Directory /path/to/your/project/staticfiles>
    Require all granted
</Directory>
```

#### For Nginx:
```nginx
location /media/ {
    alias /path/to/your/project/media/;
}

location /static/ {
    alias /path/to/your/project/staticfiles/;
}
```

### 6. Environment Variables
**Problem**: DEBUG or other settings not configured for production
**Solution**: Set proper environment variables

```bash
export DEBUG=False
export DJANGO_SETTINGS_MODULE=tjhlavnice.settings
```

### 7. Check Server Logs
**Problem**: Need to see exact error
**Solution**: Check server error logs

```bash
# Apache
tail -f /var/log/apache2/error.log

# Nginx + uWSGI
tail -f /var/log/uwsgi/tjhlavnice.log
```

## Quick Testing Commands

### Test on production server:
```bash
# Check if site is accessible
curl -I http://tjhlavnice.cz/

# Test news page specifically
curl -I http://tjhlavnice.cz/news/

# Test gallery page specifically  
curl -I http://tjhlavnice.cz/gallery/

# Check Django admin (should work)
curl -I http://tjhlavnice.cz/admin/
```

### Debug in Django shell:
```python
python manage.py shell

# Test models
from football.models import News, Gallery
print("News count:", News.objects.count())
print("Gallery count:", Gallery.objects.count())

# Test first news item
if News.objects.exists():
    news = News.objects.first()
    print("News title:", news.title)
    print("News image:", news.image)
    print("Has image:", bool(news.image))
    if news.image:
        print("Image URL:", news.get_image_url())

# Test views
from django.test import Client
client = Client()
response = client.get('/news/')
print("News response status:", response.status_code)
response = client.get('/gallery/')
print("Gallery response status:", response.status_code)
```

## Most Likely Solutions

1. **Run collectstatic**: `python manage.py collectstatic --noinput`
2. **Check media directory permissions**: `chmod -R 755 media/`
3. **Configure web server** to serve media and static files
4. **Check if all dependencies are installed**: `pip install -r requirements.txt`
5. **Restart web server** after making changes

The error 500 is now handled more gracefully with the improved error handling in views and models.
