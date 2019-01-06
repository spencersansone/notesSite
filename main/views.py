from django.shortcuts import render, redirect
from .models import *
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

def check_if_authorized(user):
    if user.username != "admin":
        return False
    return True

def getTodayDateTime():
    return datetime.now()
    
def home(request):
    x = {}
    if request.is_ajax() and request.method == "GET":
        if "get_info" in request.GET:
            note_pk = request.GET.get('note_pk')
            certain_note = Note.objects.get(id=note_pk)
            
            x['title'] = certain_note.title
            x['content'] = certain_note.content
            
            return JsonResponse(x)
        elif "is_same_check" in request.GET:
            title = request.GET.get('current_title')
            content = request.GET.get('current_content')
            pk = request.GET.get('note_pk')
            
            certain_note = Note.objects.get(id=pk)
            
            # if text, title, and cat are all the same then do nothing
            title_altered = certain_note.title != title
            # category_altered = certain_note.category != category
            content_altered = certain_note.content != content
    
            any_altered = (title_altered or content_altered)
            
            if not any_altered:
                return HttpResponse('identical')
            else:
                return HttpResponse('different')
        elif "get_datetime_edited" in request.GET:
            pass
            pk = request.GET.get('note_pk')
            certain_note = Note.objects.get(id=pk)
            if certain_note.datetime_edited.strftime('%p') == "AM":
                meridiem = "a.m."
            else:
                meridiem = "p.m."
                
            response = certain_note.datetime_edited.strftime("%b. %-d, %Y, %-I:%M " + meridiem)
            return HttpResponse(response)
            # Jan. 6, 2019, 12:33 a.m.
            # %b %-d, %Y, %-I:%-M %p
            
    elif request.is_ajax() and  request.method == "POST":
        if "save" in request.POST:
            title = request.POST.get('title')
            content = request.POST.get('content')
            pk = request.POST.get('note_pk')
            certain_note = Note.objects.get(id=pk)
            
            # if text, title, and cat are all the same then do nothing
            title_altered = certain_note.title != title
            # category_altered = certain_note.category != category
            content_altered = certain_note.content != content
    
            any_altered = (title_altered or content_altered)
            
            if not any_altered:
                return HttpResponse('identical')
            
            certain_note.content = content
            certain_note.title = title
            certain_note.datetime_edited = getTodayDateTime()
            # certain_note.category = category
            certain_note.save()
            
            if title_altered:
                return HttpResponse('saved, new title')
            
            return HttpResponse('saved')
        if "add_cat" in request.POST:
            response = ""
            title = request.POST.get('title')
            certain_note_category = NoteCategory.objects.filter(title=title)
            if len(certain_note_category) == 0:
                NoteCategory.objects.create(
                    title=title)
                return HttpResponse('pass', status=200)
            else:
                return HttpResponse('fail', status=409)
        if "delete_note" in request.POST:
            response = ""
            pk = request.POST.get('note_pk')
            title_attempt = request.POST.get('title_attempt')
            
            certain_note = Note.objects.get(id=pk)
            
            if title_attempt == certain_note.title:
                certain_note.delete()
                return HttpResponse('pass', status=200)
            else:
                return HttpResponse('fail', status=409)
            
    all_notes = Note.objects.all().order_by('title')
    all_note_categories = NoteCategory.objects.all().order_by('title')
    l = []
    
    for category in all_note_categories:
        certain_notes = all_notes.filter(category = category)
        l += [[category,certain_notes]]
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
