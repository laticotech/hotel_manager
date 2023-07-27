from django.contrib import admin
from .models import *

# Register your models here.

class FoodImageInline(admin.TabularInline):
    model = FoodImages
    extra = 5


class FoodAdmin(admin.ModelAdmin):
    list_display = ['food_name', 'food_image_tag']
    list_filter = ['food_name']
    readonly_fields = ('food_image_tag',)
    inlines = [FoodImageInline]
    prepopulated_fields = {'slug': ('food_name',)}




admin.site.register(Food, FoodAdmin)
admin.site.register(FoodImages)
