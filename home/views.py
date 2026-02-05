from django.shortcuts import render, redirect 
from .models import Slider
from .models import Slider, DiscountBanner
from .models import DiscountBanner, AboutWelcome, AboutFeature, AboutImage, Feature
from .models import ContactInfo, ContactMessage
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import ContactForm
from .models import ContactInfo
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


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



#----------------------about------------------------

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



#----------------------contact------------------------
def contact(request):
    discount = DiscountBanner.objects.filter(is_active=True).first()
    features_section1 = Feature.objects.filter(section='section1')
    features_section2 = Feature.objects.filter(section='section2')
    contact_info = ContactInfo.objects.first()
    form = ContactForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"/login/?next={request.path}")  # 👈 برگشت به contact بعد لاگین
        

        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.name = request.user.username  # 👈 گرفتن نام از یوزر
            message.save()
            return redirect('order:success')

    else:
        form = ContactForm()    

    context = {
        'discount': discount,
        'features_section1': features_section1,
        'features_section2': features_section2,
        'contact_info': contact_info,
        'form':form,
        
    }
    return render(request, 'home/contact.html', context)





