from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(
        max_length=100,
        validators=[RegexValidator(regex=r'^[^\d]+$', message='Name must not contain numbers.')]
    )
    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(regex=r'^01[0-9]{9}$', message='Enter a valid Egyptian phone number.')]
    )

    def __str__(self):
        return self.name


