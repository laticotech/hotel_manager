from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .filters import RoomFilter
from django.core.paginator import Paginator
import json
import os
import datetime
from accounts.models import *
from home.models import *
from .models import *
from datetime import datetime
import xlwt



# Create your views here.
def index(request):
    return HttpResponse('index')


def room_list(request):
    setting = Settings.objects.get(pk=1)
    list = Room.objects.all().order_by('?')
    current_user = request.user
    count_orders = OrderRoom.objects.filter(user_id=current_user.id).count()
    count_rooms = Room.objects.all().count()
    room="room"
    comments = Comment.objects.all().order_by('?')[:1]  # blog posts

    context = {'setting': setting, 'list': list, 'count_rooms': count_rooms,
               'room': room, 'count_orders': count_orders, 'comments': comments}

    # filter
    filtered_room = RoomFilter(
        request.GET,
        queryset=Room.objects.all().order_by('-id')
    )
    count = filtered_room.qs.count()

    context['filtered_room'] = filtered_room
    context['count'] = count

    # pagination
    paginated_room = Paginator(filtered_room.qs, 6)
    page_number = request.GET.get('page')
    room_page_obj = paginated_room.get_page(page_number)

    context['room_page_obj'] = room_page_obj

    return render(request, 'our_rooms.html', context=context)

def aboutroom(request, id, slug):
    current_user = request.user
    count_orders = OrderRoom.objects.filter(user_id=current_user.id).count()
    setting = Settings.objects.get(pk=1)
    viewRoom = Room.objects.get(pk=id)
    others = RoomImages.objects.filter(category_id=id)
    list = Room.objects.all().order_by('?')
    context = {'setting': setting, 'viewRoom': viewRoom, 'others': others,
               'list': list, 'count_orders': count_orders}
    return render(request, 'room_details.html', context)


@login_required(login_url='/login')
def bookThis(request, id):
    current_user = request.user
    count_orders = OrderRoom.objects.filter(user_id=current_user.id).count()
    setting = Settings.objects.get(pk=1)
    viewRoom = Room.objects.get(pk=id)
    others = RoomImages.objects.filter(category_id=id)
    list = Room.objects.all().order_by('?')
    context = {'setting': setting,  'list': list, 'viewRoom': viewRoom,
               'others': others, 'count_orders': count_orders}
    return render(request, 'book_this.html', context)



@login_required(login_url='/login')
def addtoroomcart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user
    checkroom = Booking.objects.filter(room_id=id)

    if checkroom:
        control = 1
    else:
        control = 0

    if request.method == 'POST':  # check post
        form = BookForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = Booking.objects.get(room_id=id)  # create relation with mode
                data.children = form.cleaned_data['children']
                data.adult = form.cleaned_data['adult']
                data.check_in = form.cleaned_data['check_in']
                data.check_out = form.cleaned_data['check_out']
                data.save()  # save data to table

            else:
                data = Booking()
                data.user_id = current_user.id
                data.room_id = id
                data.children = form.cleaned_data['children']
                data.adult = form.cleaned_data['adult']
                data.check_in = form.cleaned_data['check_in']
                data.check_out = form.cleaned_data['check_out']
                data.save()
        messages.success(request, f'You have successfully booked our {data.room} at GHC{data.room.daily_charge} per night. '
                                   f'You will check in on {data.check_in.date()} and check out on {data.check_out.date()}.'
                                   f' You are therefore staying for {data.diff} days at a cost of GHC{data.amount}. Thank you!')
        # return HttpResponseRedirect(url)  # redirect to contact page after submitting message
        return HttpResponseRedirect('/booked_details')  # redirect to contact page after submitting message

    else:

        if control == 1:
            data = Booking.objects.get(room_id=id)
            data.children = ['children']
            data.adult = ['adult']
            data.check_in = ['check_in']
            data.check_out = ['check_out']
            data.save()
        else:
            data = Booking()
            data.user_id = current_user.id
            data.room_id = id
            data.children = ['children']
            data.adult = ['adult']
            data.check_in = ['check_in']
            data.check_out = ['check_out']
            data.save()
        messages.success(request,  f'You have successfully booked our {data.room} at GHC{data.room.daily_charge} per night. '
                                   f'You will check in on {data.check_in.date()} and check out on {data.check_out.date()}. '
                                   f' You are therefore staying for {data.diff} days at a cost of GHC{data.amount}. Thank you!')
        return HttpResponseRedirect(url)  # redirect to contact page after submitting message



@login_required(login_url='/login')   # shopping for only members
def bookedCart(request):
    setting = Settings.objects.get(pk=1)
    current_user = request.user
    booking = Booking.objects.filter(user_id=current_user.id)
    count_orders = OrderRoom.objects.filter(user_id=current_user.id).count()
    list = Room.objects.all().order_by('?')
    total = 0
    for rs in booking:
        total += rs.amount

    context = {'booking': booking, 'setting': setting, 'total': total,
               'list': list, 'count_orders': count_orders}
    return render(request, 'booked_details.html', context)


@login_required(login_url='/login')   # shopping for only members
def deletefromcart(request, id):
    Booking.objects.filter(id=id).delete()
    messages.success(request, "Room sucessfully Deleted!")
    return HttpResponseRedirect("/booked_details")



@login_required(login_url='/login')   # shopping for only members
def orderroom(request):
    current_user = request.user
    booking = Booking.objects.filter(user_id=current_user.id)
    setting = Settings.objects.get(pk=1)
    count_orders = OrderRoom.objects.all().count()
    total = 0
    for rs in booking:
        total += rs.amount

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            # You can add credit card infor here
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            booking = Booking.objects.filter(user_id=current_user.id)
            for rs in booking:
                detail = OrderRoom()
                detail.order_id = data.id
                detail.room_id = rs.room_id
                detail.user_id = current_user.id
                detail.amount = rs.amount
                detail.save()

                room = Room.objects.get(id=rs.room_id)
                # room.amount -= rs.quantity
                room.save()

            Booking.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(request, "Your order has been completed. Thank You!")
            return render(request, 'order_completed.html', {'ordercode': ordercode, 'setting': setting,
                                                            'count_orders': count_orders})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("rooms/orderroom")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    count_orders = OrderRoom.objects.filter(user_id=current_user.id).count()
    context = {'booking': booking, 'total': total, 'setting': setting,  'form': form,
               'profile': profile, 'count_orders': count_orders}
    return render(request, 'order_form.html', context)



@login_required(login_url='/login')   # shopping for only members
def ordered_rooms(request):
    setting = Settings.objects.get(pk=1)
    current_user = request.user
    booking = Booking.objects.filter(user_id=current_user.id)
    count_orders = OrderRoom.objects.filter(user_id=current_user.id).count()
    ordered = OrderRoom.objects.filter(user_id=current_user.id).order_by('-id')
    list = Room.objects.all().order_by('?')


    context = {'ordered': ordered, 'setting': setting,
               'list': list, 'count_orders': count_orders, 'booking': booking}
    return render(request, 'my_ordered_rooms.html', context)
