from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('addtoroomcart/<int:id>', views.addtoroomcart, name='addtoroomcart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('orderroom/', views.orderroom, name='orderroom'),

]
