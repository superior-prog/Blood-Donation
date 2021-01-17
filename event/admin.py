from django.contrib import admin
from .models import *


admin.site.register(EventModel)
admin.site.register(EventInvitationModel)
admin.site.register(EventMemberModel)
