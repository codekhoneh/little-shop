from django.urls import path
from .import views
name='home'
urlpatterns = [
    path('',views.home,name='home')
    ,path('about/',views.about,name='about')
]