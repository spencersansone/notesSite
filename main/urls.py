from . import views
from django.conf.urls import url

app_name = 'main'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add_note/$', views.add_note, name='add_note'),
    url(r'^note_list/$', views.note_list, name='note_list'),
    url(r'^note_detail/(?P<pk>[0-9]+)/$', views.note_detail, name='note_detail'),
    url(r'^edit_note/(?P<pk>[0-9]+)/$', views.edit_note, name='edit_note'),
]