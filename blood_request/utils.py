from django.core.mail import send_mail
from user.models import ProfileModel


def send_notification(request):
    profiles = ProfileModel.objects.filter(blood_group=request.blood_group)

    subject = "New Blood Request For " + request.blood_group
    message = ""
    from_email = 'officialjobland777@gmail.com'
    email_list = []
    for profile in profiles:
        email_list.append(profile.user.email)

    send_mail(
        subject,
        message,
        from_email,
        email_list,
        # the mail address that the email will be sent to
    )

    return
