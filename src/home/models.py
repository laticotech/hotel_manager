from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.forms import ModelForm, TextInput, Textarea
from embed_video.fields import EmbedVideoField
from django.utils.safestring import mark_safe
from django.utils.crypto import get_random_string




# Create your models here.
class Settings(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    organization = models.CharField(max_length=50)
    address = models.CharField(blank=True, max_length=100)
    mobile = models.CharField(blank=True, max_length=50)
    phone = models.CharField(blank=True, max_length=50)
    email = models.CharField(blank=True, max_length=50)
    logo = models.ImageField(blank=True, upload_to='images/')
    motto = models.CharField(blank=True, max_length=150)
    vision = models.CharField(blank=True, max_length=300)
    mission = models.CharField(blank=True, max_length=300)
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    telegram = models.CharField(blank=True, max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    whatsapp = models.CharField(blank=True, max_length=50)
    about = RichTextUploadingField(blank=True)
    about_video = EmbedVideoField(blank=True)
    sample_about = RichTextUploadingField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Settings'


class ContactMessage(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Read', 'Read'),
    )

    name = models.CharField(blank=True, max_length=100)
    email = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=30)
    subject = models.CharField(blank=True, max_length=100)
    message = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    note = models.CharField(blank=True, max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Contact Messages'



class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message', 'subject']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'Your Fullname'}),
            'email': TextInput(attrs={'class': 'input', 'placeholder': 'Email Address'}),
            'phone': TextInput(attrs={'class': 'input', 'placeholder': 'Phone Number'}),
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Subject'}),
            'message': Textarea(attrs={'class': 'input', 'placeholder': 'Your Message'}),
        }



class Gallery(models.Model):

    title = models.CharField(blank=True, max_length=100)
    description = RichTextUploadingField()
    image = models.ImageField(blank=True, upload_to='images/')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


    def gallery_image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    gallery_image_tag.short_description = "image"

class GalleryImages(models.Model):
    category = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title


class DailyQuote(models.Model):
    author = models.CharField(blank=True, max_length=50)
    quote = models.CharField(blank=True, max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author


class Comment(models.Model):
    PUBLISH = (
        ('Publish', 'Publish'),
        ('Not Publish', 'Not Publish'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )

    name = models.CharField(max_length=30)
    email = models.CharField(blank=True, max_length=50)
    phone = models.CharField(blank=True, max_length=10)
    address = models.CharField(blank=True, max_length=255)
    subject = models.CharField(blank=True, max_length=50)
    comments = models.CharField(max_length=255)
    image = models.ImageField(default='default.png', blank=True, upload_to='images/')
    status = models.CharField(max_length=15, choices=PUBLISH, default='Not Publish')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'phone', 'address', 'subject', 'comments']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'Full Name'}),
            'email': TextInput(attrs={'class': 'input', 'placeholder': 'Email Address'}),
            'phone': TextInput(attrs={'class': 'input', 'placeholder': 'Phone Number'}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': 'City and Country'}),
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Subject'}),
            'comments': Textarea(attrs={'class': 'input', 'placeholder': 'Your Comments About Us', 'rows': '10'}),
        }


class Staff(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Transfer', 'Transfer'),
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),

    )
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    DESIGNATION = (
        ('Administrator', 'Administrator'),
        ('Director', 'Director'),
        ('Accountant', 'Accountant'),
        ('Secretary', 'Secretary'),
        ('Security', 'Security'),
        ('Janitor', 'Janitor'),
        ('Cook', 'Cook'),
        ('Other', 'Other'),

    )

    staff_id = models.CharField(max_length=10, editable=True, default=get_random_string(10))
    first_name = models.CharField(blank=True, max_length=50)
    surname = models.CharField(blank=True, max_length=50)
    dateofbirth = models.DateField(blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default='Gender')
    image = models.ImageField(upload_to='staff/', default='staff.png', blank=True, null=True)
    designation = models.CharField(blank=True, max_length=50, choices=DESIGNATION, default='Other')
    contact = models.CharField(max_length=20, blank=True, null=True)
    contact2 = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + self.surname

    class Meta:
        verbose_name_plural = 'Staff'

