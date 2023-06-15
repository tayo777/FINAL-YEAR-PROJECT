from django.contrib import admin
from .models import AmazonProduct
from .models import eBayProduct
from .models import UserPreference

# Register your models here.





admin.site.register(AmazonProduct)
admin.site.register(eBayProduct)
admin.site.register(UserPreference)
