from django.contrib import admin
from .models import *
from embed_video.admin import AdminVideoMixin

# Register your models here.
class SettingAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ['title', 'organization', 'update_at', 'logo']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'message', 'update_at']
    # you can only read these fields and not alter them since they're from your client
    readonly_fields = ['name', 'email', 'phone', 'message']
    list_filter = ['status', 'create_at', 'update_at']

class GalleryImageInline(admin.TabularInline):
    model = GalleryImages
    extra = 6


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'gallery_image_tag']
    list_filter = ['title']
    readonly_fields = ('gallery_image_tag',)
    inlines = [GalleryImageInline]
#
class AdminQuote(admin.ModelAdmin):
    list_display = ['author', 'quote', 'update_at']
    list_filter = ['author', 'quote']

class AdminComment(admin.ModelAdmin):
    list_display = ['name', 'subject', 'status', 'update_at']
    list_filter = ['name', 'subject']

class StaffAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'surname', 'designation', 'image']


admin.site.register(Staff, StaffAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryImages)
admin.site.register(Settings, SettingAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(DailyQuote, AdminQuote)
admin.site.register(Comment, AdminComment)
