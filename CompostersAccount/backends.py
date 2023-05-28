from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password,make_password
from django.core.exceptions import ObjectDoesNotExist
from .models import Composter

class ComposterAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            composter = Composter.objects.get(Email=email)
            print(composter.password)
            print('entered password' , password)
            print('entered hashed password' , make_password(password))
            if check_password(password, composter.password):
                return composter
        except Composter.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Composter.objects.get(pk=user_id)
        except Composter.DoesNotExist:
            return None