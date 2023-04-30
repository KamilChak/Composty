from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class ComposterManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Composter(AbstractBaseUser, PermissionsMixin):
    Email = models.EmailField(unique=True)
    OrganizationName = models.CharField(max_length=50)
    CommunityName = models.CharField(max_length=50)
    PhoneNumber = models.CharField(max_length=255)
    Location = models.PointField(srid=4326, default='POINT(0 0)')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = ['OrganizationName', 'CommunityName', 'PhoneNumber']

    groups = models.ManyToManyField('auth.Group', related_name='composter_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='composter_user_permissions')

    objects = ComposterManager()

    
    