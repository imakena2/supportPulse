from django.shortcuts import redirect

class RoleBasedRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path.startswith('/staff-dashboard/') and request.user.role != 'staff':
                return redirect('login')
            elif request.path.startswith('/create_ticket/') and request.user.role != 'customer':
                return redirect('login')
        return self.get_response(request)
