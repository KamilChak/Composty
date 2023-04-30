from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .models import Greener
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

from .models import Greener

class GreenerAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            greener = Greener.objects.get(Email=email)
            if check_password(password, greener.password):
                return greener
        except Greener.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Greener.objects.get(pk=user_id)
        except Greener.DoesNotExist:
            return None