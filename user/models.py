from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import Settings, settings
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

class CustomUser(AbstractUser):
    avatar = models.ImageField(blank=True, null=True)

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + " (" + ("not " if not self.confirmed else "") + "confirmed)"

class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.FileField()

    def __str__(self):
        return self.subject + " " + self.created_at.strftime("%B %d, %Y")

    def send(self, request):
        contents = self.contents.read().decode('utf-8')
        subscribers = Subscriber.objects.filter(confirmed=True)
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)

        for sub in subscribers:
            message = Mail(
                from_email = settings.FROM_EMAIL,
                to_emails = sub.email,
                subject = self.subject,
                html_content=contents + (
                    '<br><a href="{}/delete/?email={}&conf_num={}">Unsubscribe</a>.').format(
                        request.build_absolute_uri('/delete/'),
                        sub.email,
                        sub.conf_num
                    )
                )
            sg.send(message)
            

