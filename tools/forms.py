from django import forms
from .models import Tool
from .models import Supply
from .models import Job

class NewToolForm(forms.ModelForm):
    name = forms.CharField(widget=forms.Textarea(), max_length=255)

    class Meta:
        model = Tool
        fields = ['name', 'barcodeID', 'location']

class NewSupplyForm(forms.ModelForm):
    name = forms.CharField(widget=forms.Textarea(), max_length=255)

    class Meta:
        model = Supply
        fields = ['name', 'barcodeID', 'quantityReplenished', 'location']

class NewJobForm(forms.ModelForm):
    name = forms.CharField(widget=forms.Textarea(), max_length=255)

    class Meta:
        model = Job
        fields = ['name', 'barcodeID', 'barcode_img']