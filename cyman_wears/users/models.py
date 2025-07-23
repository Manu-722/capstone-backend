from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart_data = models.JSONField(default=list, blank=True)
    wishlist = models.JSONField(default=list, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True) 

    def __str__(self):
        return self.user.username