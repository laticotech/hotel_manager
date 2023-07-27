from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from PIL import Image
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.forms import ModelForm, TextInput, Textarea
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Food(models.Model):

    food_name = models.CharField(max_length=50)
    price = models.FloatField()
    descriptions = models.CharField(max_length=450)
    availability = models.BooleanField(default=True)
    food_image = models.ImageField(upload_to='images/', default='room.png')
    slug = models.SlugField(null=False, unique=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.food_name} is GHC {self.price} with {self.descriptions}'

    def food_image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.food_image.url))

    food_image_tag.short_description = "food_image"


    class Meta:
        verbose_name_plural = 'Add New Food'

class FoodImages(models.Model):
    category = models.ForeignKey(Food, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

