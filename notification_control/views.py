from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from blood_request.models import RequestModel
from user.models import ProfileModel
from .models import NotificationModel


@login_required(login_url='login')
def notification_view(request):
    profiles = ProfileModel.objects.exclude(blood_group=None)
    notifictions = NotificationModel.objects.all()

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

    context = {
        'profiles': profiles,
        'notification_list': notifictions,
    }
    return render(request, 'index.html', context)
