from django.db import models

# Create your models here.
class EmpInfo(models.Model):
    username = models.CharField(blank=False,max_length=25)
    email = models.EmailField(blank=False,max_length=25)
    password_first = models.CharField(blank=False, max_length=25)
    password_again = models.CharField(blank=False, max_length=25)

