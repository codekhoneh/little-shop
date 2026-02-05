from django.db import models

# Create your models here.
# home/models.py
from django.db import models

class Slider(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='sliders/')
    button_text = models.CharField(max_length=50, default="Shop Now")
    button_link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class DiscountBanner(models.Model):
    small_title = models.CharField(max_length=200)
    main_title = models.CharField(max_length=200)
    description = models.CharField(max_length=300, blank=True)
    button_text = models.CharField(max_length=50, default="Shop Now")
    button_link = models.URLField(blank=True)
    background_image = models.ImageField(upload_to='discounts/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.main_title

    

