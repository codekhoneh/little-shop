from django.urls import path
from .views import CollectionDetailView, WishlistView,toggle_wishlist
urlpatterns = [
    path('collections/<slug:slug>/',CollectionDetailView.as_view(), name='collection'),
    path('wishlist/toggle/<int:product_id>/', toggle_wishlist, name='toggle_wishlist'),
    path("wishlist/", WishlistView.as_view(), name="wishlist"),
]
