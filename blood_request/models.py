from django.db import models
# from user.models import User


class RequestModel(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    user = models.ForeignKey('user.User', null=True, on_delete=models.CASCADE)
    address = models.TextField(max_length=255)
    needed_within = models.DateField()
    phone = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=255, choices=BLOOD_GROUP_CHOICES)
    note = models.TextField(blank=True, null=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return str(self.user.name + " requested for " + self.blood_group)
        return str(self.user.name)
