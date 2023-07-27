from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from PIL import Image
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.forms import ModelForm, TextInput, Textarea
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime



# Create your models here.

class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '/'.join(full_path[::-1])

class Room(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=50)
    room_number = models.IntegerField()
    beds = models.IntegerField()
    capacity = models.IntegerField()
    daily_charge = models.FloatField()
    descriptions = models.CharField(max_length=255)
    availability = models.BooleanField(default=True)
    room_image = models.ImageField(upload_to='images/', default='room.png')
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room_name

    def room_image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.room_image.url))

    room_image_tag.short_description = "room_image"


    class Meta:
        verbose_name_plural = 'Add New Rooms'

class RoomImages(models.Model):
    category = models.ForeignKey(Room, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    children = models.IntegerField(blank=True)
    adult = models.IntegerField(blank=True)
    check_in = models.DateTimeField(blank=True)
    check_out = models.DateTimeField(blank=True)
    notes = RichTextUploadingField(blank=True)
    booked_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Booking ID: " + str(self.id)

    @property
    def diff(self):
        diff = self.check_out.date() - self.check_in.date()
        return diff.days


    @property
    def amount(self):
        return (self.room.daily_charge * self.diff)


class BookForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['children', 'adult', 'check_in', 'check_out']


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preparing', 'Preparing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=5, editable=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=150, blank=True)
    total = models.FloatField()
    status = models.CharField(max_length=30, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'phone']


class OrderRoom(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Cancelled', 'Cancelled'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=30, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room.room_name
