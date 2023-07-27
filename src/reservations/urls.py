from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addtoreservecart/<int:id>', views.addtoreservecart, name='addtoreservecart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('orderservice/', views.orderservice, name='orderservice'),
]
