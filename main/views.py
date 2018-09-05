from django.shortcuts import render
from .models import *
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def getTodayDateTime():
    return datetime.now()

def home(request):
    return render(request, 'main/home.html')

def add_note(request):
    if request.method == "POST":
        today = getTodayDateTime()
        t = request.POST.get('title')
        n_c = NoteCategory.objects.get(
            title = request.POST.get('note_category'))
        c = request.POST.get('content')
        
        Note.objects.create(
            title = t,
            category = n_c,
            content = c,
            datetime_created = today)
        return HttpResponseRedirect(reverse('main:home'))
    x = {}
    x['note_categories'] = NoteCategory.objects.all().order_by('title') 
    return render(request, 'main/add_note.html', x)

def note_list(request):
    x = {}
    x['note_list'] = Note.objects.all()
    return render(request, 'main/note_list.html', x)
    
def note_detail(request, pk):
    x = {}
    x['certain_note'] = Note.objects.get(id=pk)
    return render(request, 'main/note_detail.html', x)
# Create your views here.
