from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import CreateEventForm, InvitationForm
from .models import EventModel, EventInvitationModel
from user.models import User, ProfileModel


@login_required(login_url='login')
def event_home_view(request):
    event_list = EventModel.objects.all()

    search_keyword = request.GET.get('q')

    if search_keyword is not None:
        event_list = EventModel.objects.filter(Q(name__icontains=search_keyword)).order_by('-end_datetime')

    context = {
        'event_list': event_list
    }
    return render(request, 'event/index.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def delete_event_view(request, pk):
    event = EventModel.objects.get(id=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event-home')

    context = {
        'item': event,
    }
    return render(request, 'event/delete_event.html', context)


@login_required(login_url='login')
def event_detail_view(request, pk):
    event = EventModel.objects.get(id=pk)

    location_link = "https://maps.google.com/maps?width=100%25&amp;height=450&amp;hl=en&amp;q="

    if event.location is not None:
        locations = event.location.split(' ')
        location_link = "https://maps.google.com/maps?width=100%25&amp;height=450&amp;hl=en&amp;q="

        for location in locations:
            location_link += location + "%20"

        location_link += "&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed"

    users = User.objects.all()
    event_invitation = EventInvitationModel.objects.filter(event=event)
    # print(event_invitation)

    invited_people = []
    uninvited_people = []

    for person in event_invitation:
        invited_people.append(person.member)

    for person in users:
        if person not in invited_people and person != event.host and not person.is_staff:
            uninvited_people.append(person)

    # print(invited_people)
    # print(uninvited_people)
    # print(event.host)

    # invitation_form = InvitationForm()
    # if request.method == 'POST':
    #     invitation_form = InvitationForm(request.POST)
    #     if invitation_form.is_valid():
    #         invitation = invitation_form.save(commit=False)

    if request.GET.get('dltInvite'):
        personID = request.GET.get('dltPersonID')
        person = User.objects.get(pk=personID)

        invitation = EventInvitationModel.objects.get(event=event, member=person)
        invitation.delete()
        return redirect('event-detail', event.id)

    if request.GET.get('personID'):
        personID = request.GET.get('personID')
        person = User.objects.get(pk=personID)

        invitation = EventInvitationModel(event=event, member=person)
        invitation.save()
        return redirect('event-detail', event.id)

    context = {
        'event': event,
        'location_link': location_link,
        # 'profiles': profiles,
        # 'invitation_form': invitation_form,
        'invited_people': invited_people,
        'uninvited_people': uninvited_people,
    }
    return render(request, 'event/event_detail.html', context)
