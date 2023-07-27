from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from datetime import date
# from foods.models import Food
# from home.models import Services



# Create your models here.
class Services(models.Model):
    STATUS = (
        ('T&C Applies', 'T&C Applies'),
        ('No T&C', 'No T&C'),
    )

    title = models.CharField(max_length=100)
    descriptions = models.CharField(max_length=250)
    charge = models.FloatField()
    icon = models.ImageField(blank=True, upload_to='images/', default='serve.png')
    status = models.CharField(max_length=12, choices=STATUS, default='T&C Applies')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Add Services'

class ReservationCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    reserve_date = models.DateTimeField(blank=True)

    def __str__(self):
        return self.service.title

    class Meta:
        verbose_name_plural = 'Reservation Cart'

    # @property
    # def price(self):
    #     return self.service.charge

    @property
    def amount(self):
        return self.quantity * self.service.charge




class ReservationForm(ModelForm):
    class Meta:
        model = ReservationCart
        fields = ['quantity', 'reserve_date']


class Orders(models.Model):
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

    class Meta:
        verbose_name_plural = 'Users & Orders'


class OrdersForm(ModelForm):
    class Meta:
        model = Orders
        fields = ['first_name', 'last_name', 'address', 'phone']


class OrderService(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Cancelled', 'Cancelled'),
    )

    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    services = models.ForeignKey(Services, on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=30, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.services.title

    class Meta:
        verbose_name_plural = 'Ordered Services'