from django.shortcuts import get_object_or_404, render, redirect
from urllib3 import request 
from .models import Slider
from .models import Slider, DiscountBanner
from .models import DiscountBanner, AboutWelcome, AboutFeature, AboutImage, Feature
from .models import ContactInfo, ContactMessage
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import ContactForm
from .models import ContactInfo
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import ContactMessage, Reply

from .models import DiscountBanner, AboutWelcome, AboutFeature, AboutImage, Feature


# Create your views here.
def home(request):
    slides = Slider.objects.filter(is_active=True)
    discount = DiscountBanner.objects.filter(is_active=True).first()


    context = {
        'slides': slides,
        'discount': discount,
        'is_support': request.user.groups.filter(name='Support').exists() if request.user.is_authenticated else False,
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
        'is_support': request.user.groups.filter(name='Support').exists() if request.user.is_authenticated else False,


    }
    return render(request, 'home/about.html', context)



#----------------------contact------------------------
def contact(request):
    discount = DiscountBanner.objects.filter(is_active=True).first()
    features_section1 = Feature.objects.filter(section='section1')
    features_section2 = Feature.objects.filter(section='section2')
    contact_info = ContactInfo.objects.first()
    form = ContactForm()
    user_messages = ContactMessage.objects.filter(name=request.user.username).order_by('-submitted_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"/login/?next={request.path}")  # 👈 برگشت به contact بعد لاگین
        

        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.name = request.user.username  # 👈 گرفتن نام از یوزر
            message.email = request.user.email
            message.save()
            return redirect('contact')  # 👈 ریدایرکت به صفحه contact بعد ارسال پیام

    else:
        form = ContactForm()    

    context = {
        'discount': discount,
        'features_section1': features_section1,
        'features_section2': features_section2,
        'contact_info': contact_info,
        'form':form,
        'user_messages': user_messages,
        'is_support': request.user.groups.filter(name='Support').exists() if request.user.is_authenticated else False,

    }
    return render(request, 'home/contact.html', context)




def is_support(user):
    return user.groups.filter(name='Support').exists()


@login_required
@user_passes_test(is_support)
def support_dashboard(request):
    messages = ContactMessage.objects.all().order_by('-submitted_at')

    context = {
        'messages': messages
    }
    return render(request, 'home/support/dashboard.html', context)



@login_required
@user_passes_test(is_support)
def support_message_detail(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)

    # اگر پیام جدید است، وضعیت به 'read' تغییر کند
    if message.status == 'new':
        message.status = 'read'
        message.save()

    if request.method == 'POST':
        reply_text = request.POST.get('reply')
        if reply_text:
            # ذخیره پاسخ واقعی
            Reply.objects.create(
                message=message,
                responder=request.user,
                reply_text=reply_text
            )
            message.status = 'replied'
            message.save()
            return redirect('support_message_detail', pk=message.pk)

    return render(request, 'home/support/message_detail.html', {'message': message})

