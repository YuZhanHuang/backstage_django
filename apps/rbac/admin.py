from django.contrib import admin
from .models import Role, Permission, Rule
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(Rule)
