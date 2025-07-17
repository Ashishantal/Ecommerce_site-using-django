from django.db import models
from base.model import BaseModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.mail import send_account_activation_email



# Create your models here.

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verify = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile', blank=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

@receiver(post_save , sender = User)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance , email_token = email_token)
            email = instance.email
            send_account_activation_email(email , email_token)

    except Exception as e:
        print(e)