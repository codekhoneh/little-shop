
from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    name=models.CharField(
        max_length=100,
        verbose_name="نام محصول"
    )

    def __str__(self):
        return self.name

class Collection(models.Model):
    title_main = models.CharField(
        max_length=100,
        verbose_name="عنوان اصلی"
    )
    title_sub = models.CharField(
        max_length=150,
        verbose_name="عنوان فرعی"
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    image = models.ImageField(
        upload_to="collections/",
        blank=True,
        null=True
    )

    products = models.ManyToManyField(
        "Product",
        related_name="collections",
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title_main}-{self.title_sub}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title_main} - {self.title_sub}"

