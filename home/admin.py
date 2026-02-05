from django.contrib import admin
from .models import Slider
from .models import DiscountBanner
from .models import AboutWelcome, AboutFeature, AboutImage
from .models import Feature
from .models import ContactInfo, ContactMessage

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


#----------------------about------------------------


class AboutWelcomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'ceo_name')
admin.site.register(AboutWelcome, AboutWelcomeAdmin)


class AboutFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
admin.site.register(AboutFeature, AboutFeatureAdmin)

class AboutImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'order')
    list_editable = ('order',)
admin.site.register(AboutImage, AboutImageAdmin)


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order')
    list_editable = ('order',)
    list_filter = ('section',)
admin.site.register(Feature, FeatureAdmin)





#----------------------contact------------------------
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'email', 'address')
admin.site.register(ContactInfo, ContactInfoAdmin)


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    readonly_fields = ('name', 'email', 'message', 'submitted_at')
admin.site.register(ContactMessage, ContactMessageAdmin)