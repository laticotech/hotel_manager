from django.contrib import admin
from .models import *

# Register your models here.
class ReservationCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'service', 'quantity', 'amount', 'reserve_date']
    list_filter = ['user']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'descriptions', 'status', 'update_at']

class OrderServiceline(admin.TabularInline):
    model = OrderService
    readonly_fields = ('user', 'services', 'amount')
    can_delete = False
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'total', 'status']
    list_filter = ['status']
    readonly_fields = ('user', 'address', 'phone', 'first_name', 'last_name', 'total')
    can_delete = False
    inlines = [OrderServiceline]

class OrderServiceAdmin(admin.ModelAdmin):
    list_display = ['services', 'user',  'amount']
    list_filter = ['user']



admin.site.register(Orders, OrderAdmin)
admin.site.register(OrderService, OrderServiceAdmin)
admin.site.register(Services, ServiceAdmin)
admin.site.register(ReservationCart, ReservationCartAdmin)


