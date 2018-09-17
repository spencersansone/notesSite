from django.shortcuts import render, redirect
from .models import *
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def getTodayDateTime():
    return datetime.now()

def home(request):
    all_notes = Note.objects.all().order_by('title')
    all_note_categories = NoteCategory.objects.all().order_by('title')
    l = []
    
    for category in all_note_categories:
        certain_notes = all_notes.filter(category = category)
        l += [[category,certain_notes]]
        
    x = {}
    x['l'] = l
    return render(request, 'main/home.html', x)

def add_note(request):
    if request.method == "POST":
        today = getTodayDateTime()
        t = request.POST.get('title')
        n_c = NoteCategory.objects.get(
            title = request.POST.get('note_category'))
        c = request.POST.get('content')
        
        new_note = Note.objects.create(
            title = t,
            category = n_c,
            content = c,
            datetime_created = today)
        x = {}
        x['pk'] = new_note.pk
        return HttpResponseRedirect(reverse('main:note_detail', kwargs=x))
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
    
def edit_note(request, pk):
    certain_note = Note.objects.get(id=pk)
    if request.is_ajax():
        print(request.POST)
        title = request.POST.get('title')
        category = NoteCategory.objects.get(
            title = request.POST.get('category'))
        content = request.POST.get('content')
        
        certain_note = Note.objects.get(id=pk)
        
        # if text, title, and cat are all the same then do nothing
        title_altered = certain_note.title != title
        category_altered = certain_note.category != category
        content_altered = certain_note.content != content

        any_altered = (title_altered or category_altered or 
                        content_altered)
        
        if not any_altered:
            return HttpResponse('identical')
        
        certain_note.content = content
        certain_note.title = title
        certain_note.category = category
        certain_note.save()
        
        if title_altered:
            return HttpResponse('saved, new title')
        
        return HttpResponse('saved')
    elif request.method == "POST":
        t = request.POST.get('title')
        n_c = NoteCategory.objects.get(
            title = request.POST.get('note_category'))
        c = request.POST.get('content')
        
        certain_note.title = t
        certain_note.category = n_c
        certain_note.content = c
        certain_note.save()
        
        x = {}
        x['pk'] = pk
        return HttpResponseRedirect(reverse('main:note_detail', kwargs=x))
    else:
        x = {}
        x['certain_note'] = certain_note
        x['certain_note_category'] = certain_note.category
        x['note_categories'] = NoteCategory.objects.all().order_by('title')
        return render(request, 'main/edit_note.html', x)
        
def delete_note(request, pk):
    certain_note = Note.objects.get(id=pk)
    if request.method == 'POST':
        certain_note.delete()
        return redirect('main:home')
    else:
        x = {}
        x['certain_note'] = certain_note
        return render(request, 'main/delete_note.html', x)
# Create your views here.
