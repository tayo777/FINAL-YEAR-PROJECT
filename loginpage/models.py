from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class AmazonProduct(models.Model):
    product_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    rating = models.CharField(max_length=10)
    reviews = models.CharField(max_length=50)
    availability = models.CharField(max_length=50)
    link = models.CharField(max_length=255, default="")
    

    def __str__(self):
        return self.name
    
class eBayProduct(models.Model):
    product_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    rating = models.CharField(max_length=10)
    reviews = models.CharField(max_length=50)
    availability = models.CharField(max_length=50)
    link = models.CharField(max_length=255, default="" )

    def __str__(self):
        return self.name
    
class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(AmazonProduct, on_delete=models.CASCADE)
    product1 = models.ForeignKey(eBayProduct, on_delete=models.CASCADE)
    preference_count = models.IntegerField(default=0)