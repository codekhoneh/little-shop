from django.contrib import admin
from .models import Slider
from .models import DiscountBanner
# Register your models here.
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title',)

admin.site.register(Slider, SliderAdmin)


class DiscountBannerAdmin(admin.ModelAdmin):
    list_display = ('main_title', 'is_active')
    list_editable = ('is_active',)

admin.site.register(DiscountBanner, DiscountBannerAdmin)