from django.shortcuts import render
from django.http import HttpResponse
from .models import Tool
# Create your views here.

def home(request):
    tools = Tool.objects.all()
    return render(request, 'home.html', {'tools': tools})




 