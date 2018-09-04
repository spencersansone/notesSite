from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=10000)
    datetime_created = models.DateTimeField()

# Create your models here.
