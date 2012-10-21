from django.db import models
from django.contrib.auth.models import User

class ActivationKey(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    activation_key = models.CharField(max_length=32)
    key_expires = models.DateTimeField()