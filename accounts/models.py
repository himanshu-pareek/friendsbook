from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime


# Create your models here.
class UserProfile (models.Model):
    user = models.OneToOneField (User,on_delete=models.CASCADE)
    description = models.CharField (max_length = 100, default = '')
    city = models.CharField (max_length = 100,default = '')
    website = models.URLField (default = '')
    phone = models.CharField (max_length = 10, null = True)
    GENDER_CHOICES = (
        ('0' , 'Male'),
        ('1' , 'Female'),
        ('2' , 'other'),
        ('3' , 'Rather not say'),
    )

    gender = models.CharField(max_length = 1, choices=GENDER_CHOICES, default='3')


class Friends (models.Model):
    user1 = models.IntegerField(null = False, blank = False)
    user2 = models.IntegerField(null = False, blank = False)
    since = models.DateField(("Date"), default=datetime.date.today)
    friendship = models.IntegerField(null = False, blank = False)
    class Meta:
        unique_together = (('user1', 'user2'),)


class Message (models.Model):
    sender = models.IntegerField(null = False, blank = False)
    receiver = models.IntegerField(null = False, blank = False)
    message = models.TextField()
    send_time = models.DateTimeField(null = True)
    receive_time = models.DateTimeField(null = True)
    read_status = models.IntegerField(null = False, blank = False)




def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
