from ckeditor.fields import RichTextField
from django.db import models
from user.models import User


class EventModel(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = RichTextField()
    start_datetime = models.DateField()
    end_datetime = models.DateField()
    location = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    # createdAt = models.DateField(auto_now=True, default=timezone.now)


class EventInvitationModel(models.Model):
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    unique_together = [['event', 'member']]

    def __str__(self):
        return self.member.name


class EventMemberModel(models.Model):
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

