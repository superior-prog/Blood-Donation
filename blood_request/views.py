from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from user.models import ProfileModel
from .forms import *
from .utils import send_notification


@login_required(login_url='login')
def home_view(request):
    user = request.user
    profiles = ProfileModel.objects.all()
    request_list = RequestModel.objects.all()

    search_keyword = request.GET.get('q')

    if search_keyword is not None:
        request_list = RequestModel.objects.filter(Q(blood_group__icontains=search_keyword)).order_by('-posted_on')

    # for request_item in request_list:
    #     request_item.delete()
    # print(request_item.user.id)
    context = {
        'user': user,
        'profiles': profiles,
        'request_list': request_list
    }
    return render(request, 'request/index.html', context)


@login_required(login_url='login')
def create_request(request):
    task = "Post"
    form = PostRequestForm()
    if request.method == 'POST':
        form = PostRequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.user = request.user
            form.save()
            send_notification(new_request)
            return redirect('home')
        else:
            context = {
                'task': task,
                'form': form
            }
            return render(request, 'request/create_request.html', context)

    context = {
        'task': task,
        'form': form
    }
    return render(request, 'request/create_request.html', context)


@login_required(login_url='login')
def edit_request_view(request, pk):
    task = "Update"
    request_item = RequestModel.objects.get(id=pk)
    form = PostRequestForm(instance=request_item)
    if request.method == 'POST':
        form = PostRequestForm(request.POST, instance=request_item)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context = {
                'task': task,
                'form': form
            }
            return render(request, 'request/create_request.html', context)

    context = {
        'task': task,
        'form': form
    }
    return render(request, 'request/create_request.html', context)


def delete_request_view(request, pk):
    request_item = RequestModel.objects.get(id=pk)
    if request.method == 'POST':
        request_item.delete()
        return redirect('home')

    context = {
        'request_item': request_item,
    }
    return render(request, 'request/delete_request.html', context)


def request_detail_view(request, pk):
    request_item = RequestModel.objects.get(id=pk)

    context = {
        'request_item': request_item,
    }
    return render(request, 'request/request_detail.html', context)
