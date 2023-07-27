from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from . models import *
from home.models import *
from django.contrib.auth.models import User
from accounts.models import *



# Create your views here.
def index(request):
    return HttpResponse("Reservations")




@login_required(login_url='/login')   # shopping for only members
def addtoreservecart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user
    checkreserve = ReservationCart.objects.filter(service_id=id)
    if checkreserve:
        control = 1
    else:
        control = 0

    if request.method == 'POST':  # check post
        form = ReservationForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = ReservationCart.objects.get(service_id=id)  # create relation with mode
                data.reserve_date = form.cleaned_data['reserve_date']
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data to table

            else:
                data = ReservationCart()
                data.user_id = current_user.id
                data.service_id = id
                data.reserve_date = form.cleaned_data['reserve_date']
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request,
                         f'You have successfully reserve the service')
        # return HttpResponseRedirect(url)  # redirect to contact page after submitting message
        return HttpResponseRedirect('/reserved_services')  # redirect to contact page after submitting message

    else:

        if control == 1:
            data = ReservationCart.objects.get(service_id=id)
            data.quantity += 1
            data.reserve_date = ['reserve_date']
            data.save()
        else:
            data = ReservationCart()
            data.user_id = current_user.id
            data.service_id = id
            data.quantity += 1
            data.reserve_date = ['reserve_date']
            data.save()
        messages.success(request,
                         f'You have successfully reserve the service')
        return HttpResponseRedirect(url)  # redirect to contact page after submitting message




@login_required(login_url='/login')   # shopping for only members
def deletefromcart(request, id):
    ReservationCart.objects.filter(id=id).delete()
    messages.success(request, "Service sucessfully Deleted!")
    return HttpResponseRedirect("/reserved_services")


def ourServices(request):
    setting = Settings.objects.get(pk=1)
    services = Services.objects.all().order_by('-id')[:12]
    context = {'setting': setting, 'services': services}

    return render(request, 'our_services.html', context=context)


@login_required(login_url='/login')   # shopping for only members
def reservedCart(request):
    setting = Settings.objects.get(pk=1)
    current_user = request.user
    reservations = ReservationCart.objects.filter(user_id=current_user.id)
    service = Services.objects.all().order_by('?')
    total = 0
    for rs in reservations:
        total += rs.amount

    context = {'reservations': reservations, 'setting': setting, 'total': total,
               'service': service}
    return render(request, 'reserved_services.html', context)


@login_required(login_url='/login')   # requires login beore opening page
def reservations(request, id):
    setting = Settings.objects.get(pk=1)
    viewService = Services.objects.get(pk=id)
    services = Services.objects.all().order_by('?')
    context = {'setting': setting, 'viewService': viewService,
               'services': services}
    return render(request, 'reservations.html', context)




@login_required(login_url='/login')   # requires login beore opening page
def orderservice(request):
    current_user = request.user
    reservations = ReservationCart.objects.filter(user_id=current_user.id)
    setting = Settings.objects.get(pk=1)

    total = 0
    for rs in reservations:
        total += rs.amount

    if request.method == 'POST':
        form = OrdersForm(request.POST)

        if form.is_valid():
            # You can add credit card infor here
            data = Orders()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            orderscode = get_random_string(5).upper()
            data.code = orderscode
            data.save()

            reservations = ReservationCart.objects.filter(user_id=current_user.id)
            for rs in reservations:
                detail = OrderService()
                detail.order_id = data.id
                detail.services_id = rs.service_id
                detail.user_id = current_user.id
                detail.amount = rs.amount
                detail.save()

                services = Services.objects.get(id=rs.service_id)
                # rs.amount -= rs.quantity
                services.save()

            ReservationCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(request, "Your order has been completed. Thank You!")
            return render(request, 'service_orders_completed.html', {'orderscode': orderscode, 'setting': setting})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("reservations/orderservice")

    form = OrdersForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'reservations': reservations, 'total': total, 'setting': setting,  'form': form,
               'profile': profile}
    return render(request, 'orders_form.html', context)




@login_required(login_url='/login')   # shopping for only members
def my_reservations(request):
    setting = Settings.objects.get(pk=1)
    current_user = request.user
    reserves = ReservationCart.objects.filter(user_id=current_user.id)
    count_orders = OrderService.objects.filter(user_id=current_user.id).count()
    ordered = OrderService.objects.filter(user_id=current_user.id).order_by('-id')
    services = Services.objects.all().order_by('?')


    context = {'ordered': ordered, 'setting': setting, 'services': services,
               'count_orders': count_orders, 'reserves': reserves}
    return render(request, 'my_reservations.html', context)

