from django.contrib import admin
from .models import Collection,Product,ProductVariant,Wishlist,WishlistItem

admin.site.register(Collection)
admin.site.register(Product)
admin.site.register(ProductVariant) 
admin.site.register(Wishlist)
admin.site.register(WishlistItem)

