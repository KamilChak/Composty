from django.shortcuts import redirect

from CompostersAccount.models import Composter
from GreenersAccount.models import Greener

class AutoRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        if not request.session.session_key:
            return self.get_response(request)

        if request.path == '/' and request.session.get_expiry_age() > 0:
            user = request.user

            if isinstance(user, Composter):
                return redirect('composterHome')
            elif isinstance(user, Greener):
                return redirect('greenerHome') 

        return self.get_response(request)
