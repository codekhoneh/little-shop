from django.urls import path
from .import views
name='home'
urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('support/dashboard/', views.support_dashboard, name='support_dashboard'),
    path('support/message/<int:pk>/', views.support_message_detail, name='support_message_detail'),


]