from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.gis.db import models as gis_models
from CompostersAccount.models import Composter


class GreenerManager(BaseUserManager):
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


class Greener(AbstractBaseUser, PermissionsMixin):
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    Email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    PhoneNumber = models.CharField(max_length=255)
    Location = gis_models.PointField(srid=4326, default='POINT(0 0)')
    is_staff = models.BooleanField(default=False)
    composter = models.ForeignKey(Composter, on_delete=models.CASCADE, null=True, blank=True, related_name='composters')

    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = ['FirstName', 'LastName', 'PhoneNumber']

    groups = models.ManyToManyField('auth.Permission', related_name='greener_groups')
    user_permissions = models.ManyToManyField('auth.Group', related_name='greener_user_permissions')

    objects = GreenerManager()


class Offer(models.Model):
    sender = models.ForeignKey(Greener, on_delete=models.CASCADE)
    manure = models.FloatField()
    brown_material = models.FloatField()
    green_material = models.FloatField()
    date_range_start = models.DateField()
    date_range_end = models.DateField()

    def __str__(self):
        return f"{self.user.username}'s Compost Offer"





