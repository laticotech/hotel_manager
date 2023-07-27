from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .filters import FoodFilter
from django.core.paginator import Paginator
import json
import os
import datetime
from home.models import *
from .models import *
from datetime import datetime
import xlwt

# Create your views here.
def index(request):
    return HttpResponse('index')

def food_list(request):
    setting = Settings.objects.get(pk=1)
    list = Food.objects.all().order_by('?')
    count_rooms = Food.objects.all().count()
    comments = Comment.objects.all().order_by('?')[:1]  # blog posts
    food='food_list'

    context = {'setting': setting, 'list': list, 'count_rooms': count_rooms,
               'food': food, 'comments': comments}

    # filter
    filtered_food = FoodFilter(
        request.GET,
        queryset=Food.objects.all().order_by('-id')
    )
    count = filtered_food.qs.count()

    context['filtered_food'] = filtered_food
    context['count'] = count

    # pagination
    paginated_food = Paginator(filtered_food.qs, 6)
    page_number = request.GET.get('page')
    food_page_obj = paginated_food.get_page(page_number)

    context['food_page_obj'] = food_page_obj

    return render(request, 'food_list.html', context=context)



def aboutfood(request, id, slug):
    setting = Settings.objects.get(pk=1)
    viewFood = Food.objects.get(pk=id)
    others = FoodImages.objects.filter(category_id=id)
    list = Food.objects.all().order_by('?')
    context = {'setting': setting, 'viewFood': viewFood, 'others': others,
               'list': list}
    return render(request, 'food_details.html', context)


@login_required(login_url='/login')
def reserveFood(request):
    if request.method == 'POST':  # check post
        form = ReserveForm(request.POST)
        if form.is_valid():
            data = Reservation()  # create relation with mode
            data.fullname = form.cleaned_data['fullname']
            data.food = form.cleaned_data['food']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.number_of_tables = form.cleaned_data['number_of_tables']
            data.number_of_plates = form.cleaned_data['number_of_plates']
            data.amount = form.cleaned_data['amount']
            data.reservation_date = form.cleaned_data['reservation_date']


            data.save()  # save data to table
            messages.success(request,
                             "You have successfully reserved a table/food. Thank you!")  # flash message
            return HttpResponseRedirect('/reserve_food')  # redirect to contact page after submitting message
        else:
            messages.warning(request, form.errors)
            return redirect('reserve_food')  # redirect to contact page after submitting message

    list = Food.objects.all().order_by('?')
    setting = Settings.objects.get(pk=1)

    form = ReserveForm

    context = {'setting': setting, 'form': form, 'list':list}

    # filter
    filtered_food = FoodFilter(
        request.GET,
        queryset=Food.objects.all().order_by('-id')
    )
    count = filtered_food.qs.count()

    context['filtered_food'] = filtered_food
    context['count'] = count

    # pagination
    paginated_food = Paginator(filtered_food.qs, 6)
    page_number = request.GET.get('page')
    food_page_obj = paginated_food.get_page(page_number)

    context['food_page_obj'] = food_page_obj

    return render(request, 'reserve_food.html', context=context)

