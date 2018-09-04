from django.contrib import admin
from .models import *

class NoteCategoryList(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ['title']
admin.site.register(NoteCategory, NoteCategoryList)

class NoteList(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ['title']
admin.site.register(Note, NoteList)

# Register your models here.
