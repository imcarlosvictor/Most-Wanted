from django.db import models

# Create your models here.
class CriminalRecords(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
