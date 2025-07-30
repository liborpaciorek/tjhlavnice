from django.utils.deprecation import MiddlewareMixin
from .models import PageVisit

class PageVisitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip admin and static files
        if request.path.startswith('/admin/') or request.path.startswith('/static/') or request.path.startswith('/media/'):
            return None
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Get page name from path
        page_name = request.path.strip('/') or 'home'
        
        # Create page visit record
        try:
            PageVisit.objects.create(
                page_name=page_name,
                ip_address=ip,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]  # Limit length
            )
        except:
            # Silently fail if there's an issue (e.g., during migrations)
            pass
        
        return None
