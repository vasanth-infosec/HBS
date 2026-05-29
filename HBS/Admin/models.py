from django.db import models

# Create your models here.

class Department(models.Model):
    dep_name = models.CharField(max_length=100,default="No Department Exists")
    desc = models.CharField(max_length=300)
    