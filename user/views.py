from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import *
from .models import *
from .utils import calculate_age

from blood_request.models import RequestModel
from event.models import EventModel


def login_view(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')

    form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'user/login.html', context)


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = request.POST['email']
            password = request.POST['password1']
            user = authenticate(request, email=email, password=password)
            ProfileModel.objects.create(user=user)
            login(request, user)
            return redirect('home')
        else:
            context = {
                'form': form
            }
            return render(request, 'user/register.html', context)
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile_view(request, pk):
    users = User.objects.all()
    user = User.objects.get(id=pk)
    profile = ProfileModel.objects.get(user=user)

    request_list = RequestModel.objects.filter(user=user)
    events = EventModel.objects.filter(host=user)
    date_joined = calculate_age(user.date_joined)

    age = None
    if profile.birth_date:
        age = calculate_age(profile.birth_date)

    search_keyword = request.GET.get('q')

    if search_keyword is not None:
        request_list = RequestModel.objects.filter(Q(blood_group__icontains=search_keyword)).order_by('-posted_on')

        profiles = ProfileModel.objects.all()

        context = {
            'profiles': profiles,
            'request_list': request_list
        }
        return render(request, 'request/index.html', context)

    context = {
        'users': users,
        'user': user,
        'age': age,
        'profile': profile,
        'request_list': request_list,
        'total_requests': request_list.count(),
        'events': events,
        'total_events': events.count(),
        'date_joined': date_joined,
    }
    return render(request, 'user/profile.html', context)


@login_required(login_url='login')
def edit_profile_view(request):
    profile = ProfileModel.objects.get(user=request.user)

    age = None
    if profile.birth_date:
        age = calculate_age(profile.birth_date)

    form = EditProfileForm(instance=profile)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.id)
        else:
            return redirect('edit-profile')

    search_keyword = request.GET.get('q')

    if search_keyword is not None:
        request_list = RequestModel.objects.filter(Q(blood_group__icontains=search_keyword)).order_by('-posted_on')

        profiles = ProfileModel.objects.all()

        context = {
            'profiles': profiles,
            'request_list': request_list
        }
        return render(request, 'request/index.html', context)

    context = {
        'age': age,
        'form': form,
        'profile': profile,
    }
    return render(request, 'user/edit-profile.html', context)


@login_required(login_url='login')
def settings_view(request):
    user = request.user

    information_form = AccountInformationForm(instance=user)
    password_form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        information_form = AccountInformationForm(request.POST, instance=user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if information_form.is_valid():
            information_form.save()
            return redirect('profile', request.user.id)

        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile', request.user.id)
        else:
            context = {
                'information_form': information_form,
                'password_form': password_form,
            }
            return render(request, 'user/settings.html', context)

    search_keyword = request.GET.get('q')

    if search_keyword is not None:
        request_list = RequestModel.objects.filter(Q(blood_group__icontains=search_keyword)).order_by('-posted_on')

        profiles = ProfileModel.objects.all()

        context = {
            'profiles': profiles,
            'request_list': request_list
        }
        return render(request, 'request/index.html', context)

    context = {
        'information_form': information_form,
        'password_form': password_form,
    }
    return render(request, 'user/settings.html', context)


def contact_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email_add = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        send_mail(
            subject + " from " + name + " " + email_add,
            message,
            email_add,
            ['officialjobland777@gmail.com', ],
            # the mail address that the email will be sent to
        )
        messages.success(request, "Feedback sent successfully.")

        return render(request, 'user/contact.html')

    search_keyword = request.GET.get('q')

    if search_keyword is not None:
        request_list = RequestModel.objects.filter(Q(blood_group__icontains=search_keyword)).order_by('-posted_on')

        profiles = ProfileModel.objects.all()

        context = {
            'profiles': profiles,
            'request_list': request_list
        }
        return render(request, 'request/index.html', context)

    return render(request, 'contact.html')


@login_required(login_url='login')
def notification_view(request):
    search_keyword = request.GET.get('q')

    if search_keyword is not None:
        request_list = RequestModel.objects.filter(Q(blood_group__icontains=search_keyword)).order_by('-posted_on')

        profiles = ProfileModel.objects.all()

        context = {
            'search_keyword': search_keyword,
            'profiles': profiles,
            'request_list': request_list
        }
        return render(request, 'request/index.html', context)

    return render(request, 'notification.html')


@login_required(login_url='login')
def donor_view(request):
    profiles = ProfileModel.objects.exclude(blood_group=None).order_by('blood_group')

    search_keyword = request.GET.get('q')

    if search_keyword is not None:
        donor_list = ProfileModel.objects.filter(Q(blood_group__icontains=search_keyword))

        context = {
            'search_keyword': search_keyword,
            'profiles': profiles,
            'donor_list': donor_list
        }
        return render(request, 'donors.html', context)

    context = {
        'profiles': profiles,
    }
    return render(request, 'donors.html', context)
