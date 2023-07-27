from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status', 'image']
    list_filter = ['parent']

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

class RoomImageInline(admin.TabularInline):
    model = RoomImages
    extra = 5


class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_name', 'room_number', 'availability', 'room_image_tag']
    list_filter = ['room_name']
    readonly_fields = ('room_image_tag',)
    inlines = [RoomImageInline]


class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'amount', 'check_in', 'check_out']
    list_filter = ['user']

class OrderRoomline(admin.TabularInline):
    model = OrderRoom
    readonly_fields = ('user', 'room', 'amount')
    can_delete = False
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'total', 'status']
    list_filter = ['status']
    readonly_fields = ('user', 'address', 'phone', 'first_name', 'last_name', 'total')
    can_delete = False
    inlines = [OrderRoomline]

class OrderRoomAdmin(admin.ModelAdmin):
    list_display = ['room', 'user',  'amount']
    list_filter = ['user']


admin.site.register(Category, CategoryAdmin2)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderRoom, OrderRoomAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(RoomImages)
