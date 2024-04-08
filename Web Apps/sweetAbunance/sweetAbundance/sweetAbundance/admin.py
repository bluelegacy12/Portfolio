from django.contrib import admin
from .models import *

admin.site.register(Account)
admin.site.register(Product)
admin.site.register(Flavor)
admin.site.register(Review)