from django.contrib import admin
from .models import Employees,Products,Requests,Rooms,Cart

# Register your models here.
admin.site.register(Employees)
admin.site.register(Products)
admin.site.register(Requests)
admin.site.register(Rooms)
admin.site.register(Cart)
