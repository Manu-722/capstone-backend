from django.db import models
from django.contrib.auth.models import User

class Shoe(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='shoes/')
    description = models.TextField()

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.shoe.price * self.quantity

    def discounted_price(self):
        if self.quantity >= 2:
            return self.total_price() * 0.93  # 7% discount
        return self.total_price()