from django.contrib import admin
from .models import CaclValuesTbl, Basiccompanyinfo, Dailyshareinfo

# Register your models here.
admin.site.register(CaclValuesTbl)
admin.site.register(Basiccompanyinfo)
admin.site.register(Dailyshareinfo)