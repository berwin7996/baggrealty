from django.db import models

# Create your models here.
class Tenant(models.Model):
    ssn = num_stars = models.IntegerField()
    name = models.CharField(max_length=50)
    phone = num_stars = models.IntegerField()
    leasestart = models.DateField('lease start', auto_now_add=True)
    leaseend = models.DateField('lease end', auto_now_add=True)
    leasecopy = models.CharField(max_length=100)
