from django.shortcuts import render
from .models import Slider
from .models import Slider, DiscountBanner
from .models import DiscountBanner, AboutWelcome, AboutFeature, AboutImage, Feature



# Create your views here.
def home(request):
    slides = Slider.objects.filter(is_active=True)
    discount = DiscountBanner.objects.filter(is_active=True).first()

    context = {
        'slides': slides,
        'discount': discount
    }
    return render(request, 'home/index.html', context)

from django.shortcuts import render


from .models import DiscountBanner, AboutWelcome, AboutFeature, AboutImage

def about(request):
    discount = DiscountBanner.objects.filter(is_active=True).first()
    welcome = AboutWelcome.objects.first()
    features = AboutFeature.objects.all()
    images = AboutImage.objects.all()
    features_section1 = Feature.objects.filter(section='section1')
    features_section2 = Feature.objects.filter(section='section2')

    context = {
        'discount': discount,
        'welcome': welcome,
        'features': features,
        'images': images,
        'features_section1': features_section1,
        'features_section2': features_section2,

    }
    return render(request, 'home/about.html', context)



