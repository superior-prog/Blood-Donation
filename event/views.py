from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import CreateEventForm
from .models import EventModel


def event_home_view(request):
    event_list = EventModel.objects.all()

    search_keyword = request.GET.get('q')

    if search_keyword is not None:
        event_list = EventModel.objects.filter(Q(name__icontains=search_keyword)).order_by('-end_datetime')

    context = {
        'event_list': event_list
    }
    return render(request, 'event/index.html', context)


def create_event_view(request):
    task = "Create"
    form = CreateEventForm()
    if request.method == 'POST':
        form = CreateEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user
            form.save()
            return redirect('event-home')
        else:
            context = {
                'task': task,
                'form': form
            }
            return render(request, 'request/create_event.html', context)

    context = {
        'task': task,
        'form': form
    }
    return render(request, 'event/create_event.html', context)


def edit_event_view(request, pk):
    task = "Update"
    event = EventModel.objects.get(id=pk)
    form = CreateEventForm(instance=event)
    if request.method == 'POST':
        form = CreateEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event-detail', event.id)
        else:
            context = {
                'task': task,
                'form': form,
            }
            return render(request, 'event/create_event.html', context)

    context = {
        'task': task,
        'form': form,
    }
    return render(request, 'event/create_event.html', context)


def delete_event_view(request, pk):
    # blog = BlogModel.objects.get(slug=slug)
    # if request.method == 'POST':
    #     blog.delete()
    #     return redirect('blogs', request.user.id)

    context = {
        # 'item': blog,
    }
    return render(request, 'delete-blog.html', context)


def event_detail_view(request, pk):
    event = EventModel.objects.get(id=pk)

    context = {
        'event': event,
    }
    return render(request, 'event/event_detail.html', context)
