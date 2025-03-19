# from datetime import datetime
# from django.utils.deprecation import MiddlewareMixin
# from .models import SiteHit

# class SiteHitMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if request.path.startswith('/admin/'):
#             return  # Ignore admin hits

#         SiteHit.objects.create(
#             ip_address=self.get_client_ip(request),
#             path=request.path,
#             timestamp=datetime.now()
#         )

#     def get_client_ip(self, request):
#         """Extracts client IP from request headers."""
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         return ip
