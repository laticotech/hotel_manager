"""smarthotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from home import views
from accounts import views as AccountViews
from rooms import views as RoomViews
from foods import views as FoodViews
from reservations import views as ReservationViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('rooms/', include('rooms.urls')),
    path('foods/', include('foods.urls')),
    path('reservations/', include('reservations.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # home urls
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contactus/', views.contactus, name='contactus'),
    path('our_gallery/', views.gallery, name='our_gallery'),
    path('our_staff/', views.staffs, name='our_staff'),
    path('your_comments/', views.yourComments, name='your_comments'),

    # Rooms
    path('our_rooms/', RoomViews.room_list, name='our_rooms'),
    path('book_this/<int:id>', RoomViews.bookThis, name='book_this'),
    path('room_details/<int:id>', RoomViews.aboutroom, name='room_details'),
    path('booked_details/', RoomViews.bookedCart, name='booked_details'),
    path('my_ordered_rooms/', RoomViews.ordered_rooms, name='my_ordered_rooms'),

    # Food
    path('food_list/', FoodViews.food_list, name='food_list'),
    path('reserve_food/', FoodViews.reserveFood, name='reserve_food'),
    path('food_details/<int:id>/<slug:slug>', FoodViews.aboutfood, name='food_details'),

    # Users urls
    path('register/', AccountViews.register, name='register'),
    path('profile/', AccountViews.profile, name='profile'),
    path('profile_update/', AccountViews.profileUpdate, name='profile_update'),
    path('login/', AccountViews.loginform, name='login'),
    path('login2/', auth_views.LoginView.as_view(template_name='login2.html'), name='login2'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('logout2/', AccountViews.logoutfunc, name='logoutfunc'),


    # Reservations urls   reservedCart
    path('reservations/<int:id>/', ReservationViews.reservations, name='reservations'),
    path('our_services/', ReservationViews.ourServices, name='our_services'),
    path('reserved_services/', ReservationViews.reservedCart, name='reserved_services'),
    path('my_reservations/', ReservationViews.my_reservations, name='my_reservations'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
