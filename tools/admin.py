from django.contrib import admin
from .models import Tool
from .models import Supply
from .models import InvUser
from .models import Job
from .models import Log
# Register your models here.

admin.site.register(Tool)
admin.site.register(Supply)
admin.site.register(InvUser)
admin.site.register(Job)
admin.site.register(Log)