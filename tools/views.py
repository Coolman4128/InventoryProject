from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from .models import Tool
from .models import Supply
from .models import InvUser
from .models import Job
from .forms import NewToolForm
from .forms import NewSupplyForm
from .forms import NewJobForm
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from cryptography.fernet import Fernet
import datetime


# Create your views here.

SCANNERKEYS = ['1234', 'SERVERREQUEST'] #THESE KEYS ARE THE DECRYPTED KEYS THAT THE SCANNER GUNS WILL SEND, KEEP SECRET
ENCRYPTEDSCANKEYS = ['', ''] # These are for testing
key = Fernet.generate_key()
fernet = Fernet(key) # Secret key from django
ENCRYPTEDSCANKEYS[0] = fernet.encrypt(SCANNERKEYS[0].encode())
LOWSUPPLYCODE = "12345678910"


def home(request):
    tools = Tool.objects.all()
    supplys = Supply.objects.all()
    return render(request, 'home.html', {'tools': tools, 'supplys': supplys})

def jobs(request):
    allJobs = Job.objects.all()
    print(allJobs[0].barcode_img.url)
    return render(request, 'jobs.html', {"jobs": allJobs})

@csrf_exempt 
def newJob(request):
    if request.method == 'POST':
        form = NewJobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.isBeingWorkedOn = False
            job.userScannedIn = ''
            job.timeScannedIn = None
            job.totalHours = 0
            job.save()
            return redirect('jobs') 
        else:
            print(form.errors)
    else:
        form = NewJobForm()
    return render(request, 'new_job.html', {'form':form})

def get_Tool(request, pk):
    tool = get_object_or_404(Tool, barcodeID=pk)
    data = serializers.serialize('json', [tool])
    return HttpResponse(data, content_type='application/json')

def get_Supply(request, pk):
    supply = get_object_or_404(Supply, barcodeID=pk)
    data = serializers.serialize('json', [supply])
    return HttpResponse(data, content_type='application/json')

def get_user(request, pk):
    user = get_object_or_404(InvUser, barcodeID=pk)
    data = serializers.serialize('json', [user])
    return HttpResponse(data, content_type='application/json')

def findType(request, pk):
    foundName = ''
    tools = Tool.objects.all()
    supplys = Supply.objects.all()
    users = InvUser.objects.all()
    jobs = Job.objects.all()

    for tool in tools:
        if tool.barcodeID == pk:
            foundName = 'tool'
            return HttpResponse(foundName)
    for supply in supplys:
        if supply.barcodeID == pk:
            foundName = 'supply'
            return HttpResponse(foundName)
    for user in users:
        if user.barcodeID == pk:
            foundName = 'user'
            return HttpResponse(foundName)
    for job in jobs:
        if job.barcodeID == pk:
            foundName = 'job'
            return HttpResponse(foundName)
    
    if pk == LOWSUPPLYCODE:
        pass
    return HttpResponse(foundName)

def check_Tool(request, pk, key, user):
    #if (fernet.decrypt(key).decode() in SCANNERKEYS):
    if (key in SCANNERKEYS):
        tool = get_object_or_404(Tool, barcodeID=pk)
        if (tool.isCheckedOut):
            tool.isCheckedOut = False
            tool.userCheckedOut = ''
            tool.timeCheckedOut = None
        else:
            tool.isCheckedOut = True
            tool.timeCheckedOut = timezone.now()
            tool.userCheckedOut = user
        tool.save()
        return HttpResponse(serializers.serialize('json', [tool]), content_type='application/json')
    else:
        return HttpResponse("NOT AUTHENTICATED")
    
def replenish_Supply(request, pk, key, user):
    #if (fernet.decrypt(key).decode() in SCANNERKEYS):
    if (key in SCANNERKEYS):
        supply = get_object_or_404(Supply, barcodeID=pk)
        supply.isLow = False
        supply.whoReplenished = user
        supply.lastReplenished = timezone.now()
        supply.save()
        return HttpResponse(serializers.serialize('json', [supply]), content_type='application/json')
    else:
        return HttpResponse("NOT AUTHENTICATED")
    
def scanIntoJob(request, pk, key, user):
    #if (fernet.decrypt(key).decode() in SCANNERKEYS):
    if (key in SCANNERKEYS):
        job = get_object_or_404(Job, barcodeID=pk)
        s = "-"
        if (job.isBeingWorkedOn):
            usersWorking = job.userScannedIn.split("-")
            if user in usersWorking:
                usersWorking.remove(user)
                if usersWorking == []:
                    job.isBeingWorkedOn = False
                    job.userScannedIn = ""
                else:
                    job.userScannedIn = s.join(usersWorking)
                timeWorked = ((timezone.now() - job.timeScannedIn).total_seconds()) / 3600
                job.totalHours = job.totalHours + timeWorked

            else:
                usersWorking = usersWorking + [user]
                print(usersWorking)
                timeWorked = (((timezone.now() - job.timeScannedIn).total_seconds()) / 3600) * len(usersWorking)
                job.userScannedIn = s.join(usersWorking)
                job.timeScannedIn = timezone.now()
                job.totalHours = job.totalHours + timeWorked
        else:
            job.isBeingWorkedOn = True
            job.timeScannedIn = timezone.now()
            job.userScannedIn = user
        job.save()
        return HttpResponse(serializers.serialize('json', [job]), content_type='application/json')
    else:
        return HttpResponse("NOT AUTHENTICATED")
    
def low_Supply(request, pk, key):
    #if (fernet.decrypt(key).decode() in SCANNERKEYS):
    if (key in SCANNERKEYS):
        supply = get_object_or_404(Supply, barcodeID=pk)
        supply.isLow = True
        supply.save()
        return HttpResponse(serializers.serialize('json', [supply]), content_type='application/json')
    else:
        return HttpResponse("NOT AUTHENTICATED")

def del_Tool(request, pk, key):
    #if (fernet.decrypt(key).decode() in SCANNERKEYS):
    if (key in SCANNERKEYS):
        tool = get_object_or_404(Tool, barcodeID=pk)
        tool.delete()
        if (key == "SERVERREQUEST"):
            return redirect('home')
        return HttpResponse('Tool Deleted')
    else:
        return HttpResponse("NOT AUTHENTICATED")

def del_Supply(request, pk, key):
    #if (fernet.decrypt(key).decode() in SCANNERKEYS):
    if (key in SCANNERKEYS):
        supply = get_object_or_404(Supply, barcodeID=pk)
        supply.delete()
        if (key == "SERVERREQUEST"):
            return redirect('home')
        return HttpResponse('Supply Deleted')
    else:
        return HttpResponse("NOT AUTHENTICATED")

def del_Job(request, pk, key):
    #if (fernet.decrypt(key).decode() in SCANNERKEYS):
    if (key in SCANNERKEYS):
        job = get_object_or_404(Job, barcodeID=pk)
        job.delete()
        if (key == "SERVERREQUEST"):
            return redirect('jobs')
        return HttpResponse('Supply Deleted')
    else:
        return HttpResponse("NOT AUTHENTICATED")
    
def del_UI(request):
    tools = Tool.objects.all()
    supplys = Supply.objects.all()
    jobs = Job.objects.all()
    return render(request, 'delete.html', {'tools': tools, 'supplys': supplys, 'jobs': jobs})
        
@csrf_exempt 
def newTool(request):
    if request.method == 'POST':
        form = NewToolForm(request.POST)
        if form.is_valid():
            tool = form.save(commit=False)
            tool.isCheckedOut = False
            tool.userCheckedOut = ''
            tool.timeCheckedOut = None
            tool.save()
            return redirect('home')
    else:
        form = NewToolForm()
    return render(request, 'new_tool.html', {'form':form})

@csrf_exempt 
def newSupply(request):
    if request.method == 'POST':
        form = NewSupplyForm(request.POST)
        if form.is_valid():
            supply = form.save(commit=False)
            supply.isLow = False
            supply.whoReplenished = ''
            supply.save()
            return redirect('home')
    else:
        form = NewSupplyForm()
    return render(request, 'new_supply.html', {'form':form})
 