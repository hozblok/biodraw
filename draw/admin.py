from django.contrib import admin

from .models import FileOwl
from .models import PhysicalEntity

admin.site.register(FileOwl)
admin.site.register(PhysicalEntity)
