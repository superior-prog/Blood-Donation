from django.db import models


class NotificationModel(models.Model):
    title = models.TextField()
    link = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.title
