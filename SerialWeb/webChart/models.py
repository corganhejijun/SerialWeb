# -*- coding: UTF-8 -*-
from django.db import models

# Create your models here.
class Port1(models.Model):
    time = models.CharField(max_length=32)
    value = models.CharField(max_length=128)

class Port2(models.Model):
    time = models.CharField(max_length=32)
    value = models.CharField(max_length=128)

class Port3(models.Model):
    time = models.CharField(max_length=32)
    value = models.CharField(max_length=128)

class Port4(models.Model):
    time = models.CharField(max_length=32)
    value = models.CharField(max_length=128)

class PortData(models.Model):
    name = models.CharField(max_length=32)
    time = models.CharField(max_length=32)
    strValue = models.CharField(max_length=128)
