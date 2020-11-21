from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'


class categories(models.Model):
    cat_name = models.CharField(max_length=64,unique=True)



class auction_listing(models.Model):
    pro_name = models.CharField(max_length=30)
    pro_description = models.TextField()
    pro_price = models.IntegerField()
    pro_image = models.URLField(max_length=200)
    date = models.DateTimeField()
    cat_id = models.ForeignKey('categories', on_delete=models.CASCADE)
    owner_name = models.ForeignKey('User', on_delete=models.CASCADE)
    is_running = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.pro_name}"

class pro_bid(models.Model):
    owner_name = models.ForeignKey('User', on_delete=models.CASCADE)
    pro_name = models.ForeignKey('auction_listing', on_delete=models.CASCADE)
    bid_amount = models.IntegerField()

    def __str__(self):
        return f"{self.owner_name} bids on {self.pro_name} at {self.bid_amount}"

class watchlist(models.Model):
    owner_name = models.ForeignKey('User', on_delete=models.CASCADE)
    pro_name = models.ForeignKey('auction_listing', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pro_name} On Wachlist of {self.owner_name}"

class comments(models.Model):
    name = models.ForeignKey('User', on_delete=models.CASCADE)
    comment = models.TextField()
    pro_details = models.ForeignKey('auction_listing', on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f"{self.name} commented on {self.pro_details}"