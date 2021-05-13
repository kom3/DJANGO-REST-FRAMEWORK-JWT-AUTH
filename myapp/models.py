from django.db import models

# Create your models here.

class Mymodel(models.Model):
    name = models.CharField(max_length=200)
    app_label = "auth"