from django.contrib import admin
from .models import Tool
from .models import Supply
from .models import InvUser
# Register your models here.

admin.site.register(Tool)
admin.site.register(Supply)
admin.site.register(InvUser)