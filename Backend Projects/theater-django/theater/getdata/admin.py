from django.contrib import admin
from .models import Performers, Shows, Roles, CallTime, RehearsalVenues, Company, Staff

admin.site.register(Performers)
admin.site.register(Shows)
admin.site.register(Roles)
admin.site.register(CallTime)
admin.site.register(RehearsalVenues)
admin.site.register(Company)
admin.site.register(Staff)