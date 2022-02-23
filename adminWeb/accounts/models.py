from django.conf import settings 
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.template.loader import render_to_string
from django.shortcuts import resolve_url

class User(AbstractUser):
    class MembershipChoices(models.TextChoices):
        USER = "User", "User" # DB에 저장되는 값, 실제 보여지는 값
        AGENCY = "Agency", "Agency" 

    follower_set = models.ManyToManyField("self", blank=True)
    following_set = models.ManyToManyField("self", blank=True)

    membership = models.CharField(max_length=7, choices=MembershipChoices.choices, default=MembershipChoices.USER)
    phone_number = models.CharField(max_length=13, blank=True,
                                    validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}")])

    avartar = models.ImageField(blank=True, upload_to="accounts/avartar/%Y/%m/%d")
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property 
    def avartar_url(self):
        if self.avartar:
            return self.avartar_url
        else:
            return resolve_url("pydenticon_image", self.username)

    def send_welcome_email(self):
        subject = render_to_string("accounts/welcome_email_subject.txt", {
            "user":self, 
        })
        content = render_to_string("accounts/welcome_email_content.txt", {
            "user":self, 
        })
        sender_email = settings.WELCOME_EMAIL_SENDER
        send_mail(subject, content, sender_email, [self.email], fail_silently=False)
        




