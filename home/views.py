from django.shortcuts import render
from .models import Slider
from .models import Slider, DiscountBanner
def home(request):
    slides = Slider.objects.filter(is_active=True)
    discount = DiscountBanner.objects.filter(is_active=True).first()

    context = {
        'slides': slides,
        'discount': discount
    }
    return render(request, 'home/index.html', context)

# Create your views here.

