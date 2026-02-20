from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


# --------------------
# Product
# --------------------
class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def final_price(self):
        if self.discount_percent:
            return self.price - (self.price * self.discount_percent / 100)
        return self.price

    def __str__(self):
        return self.title


# --------------------
# Product Variant
# --------------------
class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=10)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.title} - {self.color} - {self.size}"

    def clean(self):
        if ProductVariant.objects.filter(
            product=self.product,
            color=self.color,
            size=self.size
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f"This color ({self.color}) and size ({self.size}) combination "
                f"already exists for {self.product.title}."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


# --------------------
# Collection
# --------------------
class Collection(models.Model):
    title_main = models.CharField(max_length=100)
    title_sub = models.CharField(max_length=150)

    slug = models.SlugField(unique=True, blank=True)

    image = models.ImageField(
        upload_to="collections/",
        blank=True,
        null=True
    )

    products = models.ManyToManyField(
        Product,
        related_name="collections",
        blank=True
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title_main}-{self.title_sub}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title_main} - {self.title_sub}"
# -------------------------------------
#             wishlist:
# -------------------------------------

class Wishlist(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s Wishlist"
    
    

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wishlist', 'product') #جلوگیری از تکرار محصول در یک لیست خواسته‌ها

    def __str__(self):
        return f"{self.product.title} in {self.wishlist.user}'s Wishlist"