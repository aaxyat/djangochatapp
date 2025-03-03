from django.contrib import admin
from server.models import Category, Channel, Server

# Register your models here.

admin.site.register(Category)
admin.site.register(Server)
admin.site.register(Channel)
