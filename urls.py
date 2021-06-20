from unicodedata import name
from django.urls import path
from . import views 


app_name = 'app_post'


urlpatterns= [
    path('',views.home,name='home'),
    path('liked/<pk>',views.liked,name='liked'),
    path('liked/<pk>/',views.unliked,name='unliked'),
]
