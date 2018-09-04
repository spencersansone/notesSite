from django.db import models

class NoteCategory(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Note(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(NoteCategory, on_delete=models.CASCADE)
    content = models.TextField(max_length=10000)
    datetime_created = models.DateTimeField()

# Create your models here.
