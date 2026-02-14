from django.shortcuts import render
from django.views.generic import DetailView
from .models import Collection
from django.core.paginator import Paginator

class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'shop/collection.html'
    context_object_name = 'collection'
    slug_field = 'slug'
    slug_url_kwarg = 'slug' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = self.object.products.filter(is_active=True,variants__stock__gt=0).distinct()
        sort = self.request.GET.get("sort")

        if sort == "price_asc":
            products = products.order_by("price")

        elif sort == "price_desc":
            products = products.order_by("-price")

        elif sort == "newest":
            products = products.order_by("-id")  # فعلاً چون created_at در Product نداریم

        else:
            # پیش‌فرض → جدیدترین
            products = products.order_by("-id")

        paginator = Paginator(products, 1) 
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj
        context["products"] = page_obj
        context["sort"] = sort

        return context