from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware(AuthenticationMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            # Check if the view is decorated with @login_not_required
            if not hasattr(view_func, '_login_not_required'):
                login_url = reverse('login') # Assuming your login URL is named 'login'
                if request.path != login_url:
                    return redirect(f"{login_url}?next={request.path}")
        return None