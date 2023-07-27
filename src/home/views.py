from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from rooms.models import *
from foods.models import *
from accounts.models import *



# Create your views here.
def index(request):

    setting = Settings.objects.get(pk=1)
    rooms = Room.objects.all()  # blog posts
    gallery = Gallery.objects.all()  # blog posts
    room_list = Room.objects.all().order_by('-id')[:12]
    food_list = Food.objects.all().order_by('-id')[:12]
    category = Category.objects.all().order_by('-id')[:12]
    daily = DailyQuote.objects.all().order_by('?')[:1]  # blog posts
    comments = Comment.objects.all().order_by('?')[:1]  # blog posts
    current_user = request.user
    count_orders = OrderRoom.objects.filter(user_id=current_user.id).count()
    home = "home"
    context = {'setting': setting, 'home': home, 'rooms': rooms,
               'room_list': room_list, 'gallery': gallery,
               'count_orders': count_orders, 'category': category,
               'food_list': food_list, 'daily': daily, 'comments': comments,
             }
    return render(request, 'index.html', context)


def contactus(request):
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # create relation with mode
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')  # give user ip address
            data.save()  # save data to table
            messages.success(request,
                             "Your message has been sent. We'll get back you as soon as possible. Thank you!")  # flash message
            return HttpResponseRedirect('/contactus')  # redirect to contact page after submitting message
        else:
            messages.warning(request, form.errors)
            return redirect('contactus')  # redirect to contact page after submitting message

    setting = Settings.objects.get(pk=1)
    form = ContactForm
    contacted = "contactus"
    pending = ContactMessage.objects.filter(status="Pending")
    total = ContactMessage.objects.all().count()
    current_user = request.user
    count_orders = OrderRoom.objects.filter(user_id=current_user.id).count()
    context = {'setting': setting, 'form': form, 'contacted': contacted, 'pending': pending,
               'total': total, 'count_orders': count_orders}
    return render(request, 'contactus.html', context)


def aboutus(request):
    setting = Settings.objects.get(pk=1)
    food_list = Food.objects.all().order_by('-id')[:12]
    current_user = request.user
    count_orders = OrderRoom.objects.filter(user_id=current_user.id).count()
    about = "aboutus"
    context = {'setting': setting, 'about': about, 'food_list': food_list,
               'count_orders':count_orders}

    return render(request, 'aboutus.html', context=context)

def gallery(request):
    setting = Settings.objects.get(pk=1)
    gallery = Gallery.objects.all()  # blog posts
    current_user = request.user
    count_orders = OrderRoom.objects.filter(user_id=current_user.id).count()
    context = {'setting': setting, 'gallery': gallery, 'count_orders':count_orders}

    return render(request, 'our_gallery.html', context=context)


def staffs(request):
    setting = Settings.objects.get(pk=1)
    staff = Staff.objects.all()  # blog posts
    current_user = request.user
    count_orders = OrderRoom.objects.filter(user_id=current_user.id).count()
    context = {'setting': setting, 'staff': staff, 'count_orders':count_orders}

    return render(request, 'our_staff.html', context=context)


def yourComments(request):
    if request.method == 'POST':  # check post
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()  # create relation with mode
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address = form.cleaned_data['address']
            data.subject = form.cleaned_data['subject']
            data.comments = form.cleaned_data['comments']
            data.ip = request.META.get('REMOTE_ADDR')  # give user ip address
            data.save()  # save data to table
            messages.success(request,
                             "Your comments has been sent. Thank you!")  # flash message
            return HttpResponseRedirect('/your_comments')  # redirect to contact page after submitting message
        else:
            messages.warning(request, form.errors)
            return redirect('your_comments')  # redirect to contact page after submitting message

    setting = Settings.objects.get(pk=1)
    comments = Comment.objects.all().order_by('?')[:1]  # blog posts
    current_user = request.user
    count_orders = OrderRoom.objects.filter(user_id=current_user.id).count()
    context = {'setting': setting, 'comments': comments, 'count_orders':count_orders}

    return render(request, 'your_comments.html', context=context)