from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.FloatField()
    images = models.ImageField(upload_to='photos/products',)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse("product_detail", args=[self.category.slug, self.slug])


    def __str__(self):
        return self.product_name


class ReviewRating(models.Model):
    user=models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True, null=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField(blank=True)
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, blank = True)

    # reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", null=True)


    class Meta:
        # sort comments in chronological order by default
        ordering = ('created_date',)

    def __str__(self):
        return self.subject

    def children(self):
        return ReviewRating.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True



class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'product gallery'
        verbose_name_plural = 'product gallery'
