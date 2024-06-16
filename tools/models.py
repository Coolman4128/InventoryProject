from django.db import models
from datetime import datetime 
from django.contrib.auth.models import User

class Tool(models.Model):
    name = models.CharField(max_length=255, unique = True)
    barcodeID = models.CharField(max_length=255, unique=True)
    isCheckedOut = models.BooleanField()
    timeCheckedOut = models.DateTimeField(null=True, blank=True)
    userCheckedOut = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length = 255)

    def __str__(self):
        return self.name


class Supply(models.Model):
    name = models.CharField(max_length=255, unique = True)
    barcodeID = models.CharField(max_length=255, unique=True)
    quantityReplenished = models.CharField(max_length=255)
    isLow = models.BooleanField(db_default=False)
    lastReplenished = models.DateTimeField(auto_now_add=True)
    whoReplenished = models.CharField(max_length=50)
    location = models.CharField(max_length = 255)

    def __str__(self):
        return self.name

class InvUser(models.Model):
    name = models.CharField(max_length=50, unique = True)

    def __str__(self):
        return self.name


