from django.db import models

# Create your models here.
class FugitiveProfiles(models.Model):
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    sex = models.CharField(max_length=255)
    height_in_cm = models.IntegerField()
    weight_in_kg = models.IntegerField()
    eyes = models.CharField(max_length=255)
    hair = models.CharField(max_length=255)
    distinguishing_marks = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=255)
    place_of_birth = models.CharField(max_length=255)
    charges = models.TextField()
    wanted_by = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    publication = models.CharField(max_length=255)
    last_modified = models.CharField(max_length=255)
    reward = models.CharField(max_length=255)
    details = models.TextField()
    caution = models.TextField(max_length=255)
    remarks = models.TextField(max_length=255)
    images = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
