from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView,ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Collection, Wishlist, WishlistItem, Product
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import apply_sort




class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'shop/collection.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = self.object.products.filter(
            is_active=True,
            variants__stock__gt=0
        ).distinct()

        sort = self.request.GET.get("sort")

        # ✅ فقط sort از utility میاد
        products = apply_sort(products, sort)

        # ✅ pagination هنوز اینجاست (داخل view)
        paginator = Paginator(products, 6)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["products"] = page_obj
        context["page_obj"] = page_obj
        context["sort"] = sort

        return context
# ---------------------------------------------------------------------
# toggle_wishlist
# ----------------------------------------------------------------------
@require_POST
def toggle_wishlist(request, product_id):

    # 🔐 اگر لاگین نبود → 401 برگردون
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "Authentication required"},
            status=401
        )

    # 📦 گرفتن محصول
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse(
            {"error": "Product not found"},
            status=404
        )

    # ❤️ گرفتن یا ساختن wishlist
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    # 🔁 Toggle حرفه‌ای
    item, created = WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )

    if not created:
        item.delete()
        status = "removed"
        message = "Removed from wishlist"
    else:
        status = "added"
        message = "Added to wishlist"

    # 🔢 تعداد آیتم‌ها
    wishlist_count = wishlist.items.count()

    return JsonResponse({
        "status": status,
        "message": message,
        "wishlist_count": wishlist_count
    })
# -----------------------------
# WishlistView
# -----------------------------
class WishlistView(LoginRequiredMixin, ListView):
    model = WishlistItem
    template_name = "shop/wishlist.html"
    context_object_name = "wishlist_items"
    login_url = "account:login"
    paginate_by = 1

    def get_queryset(self):
        wishlist = Wishlist.objects.filter(user=self.request.user).first()
        
        if not wishlist:
            return WishlistItem.objects.none()
        
        return wishlist.items.select_related("product")