# Production Deployment Guide - TJ Hlavnice

## 🔧 Error 400 Fix Applied

### Issue Resolved:
- **Problem**: Error 400 on production server
- **Cause**: Incorrect `ALLOWED_HOSTS` format with protocols
- **Solution**: Fixed domain names in settings

## 🚀 Production Server Setup

### 1. Environment Variables
Set these on your production server:

```bash
# For development
export DEBUG=True

# For production (default)
export DEBUG=False  # or don't set (defaults to False)
```

### 2. Static Files
Run on production server after deployment:

```bash
python manage.py collectstatic --noinput
```

### 3. Database Migrations
Run migrations on production:

```bash
python manage.py migrate
```

### 4. Logging
Django will create a `django.log` file in the project root for debugging issues.

## ✅ Fixed Settings

### ALLOWED_HOSTS
**Before (❌ Wrong):**
```python
ALLOWED_HOSTS = ['https://tjhlavnice.cz', 'https://www.tjhlavnice.cz/', '127.0.0.1', 'localhost']
```

**After (✅ Correct):**
```python
ALLOWED_HOSTS = ['tjhlavnice.cz', 'www.tjhlavnice.cz', '127.0.0.1', 'localhost']
```

### Security Headers Added
For production safety:
```python
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 86400
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

## 🔍 Troubleshooting

### Check Logs
- View Django logs: `tail -f django.log`
- Check production server logs for additional errors

### Common Issues:
1. **Static files not loading**: Run `collectstatic`
2. **Database errors**: Run migrations
3. **Permission issues**: Check file/directory permissions
4. **Domain not working**: Verify DNS points to correct server

### Test Commands:
```bash
# Test settings
python manage.py check --deploy

# Create superuser for admin
python manage.py createsuperuser

# Test Czech localization
python manage.py shell
>>> from django.utils.translation import gettext
>>> print(gettext('News'))  # Should print in Czech
```

## 📝 Production Checklist

- ✅ Fixed ALLOWED_HOSTS format
- ✅ Environment-based DEBUG setting  
- ✅ Security headers configured
- ✅ Logging enabled
- ✅ Czech localization working
- ✅ Rich text editor configured
- ✅ Static files configuration ready
- ✅ Database migrations ready

## 🔗 URLs to Test:

After deployment, verify these work:
- `https://tjhlavnice.cz/` - Homepage
- `https://tjhlavnice.cz/admin/` - Admin (Czech interface)
- `https://www.tjhlavnice.cz/` - Homepage with www
- `https://tjhlavnice.cz/news/` - News section
- `https://tjhlavnice.cz/club/` - Club info

**Error 400 should now be resolved!** 🎉
