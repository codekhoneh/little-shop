from django.urls import path
from .views import CollectionDetailView

urlpatterns = [
    path('collections/<slug:slug>/',CollectionDetailView.as_view(), name='collection'),
]
