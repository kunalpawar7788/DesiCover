from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Userprofile(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile= models.CharField(max_length=100)
    city  = models.CharField(max_length=2000,default='',blank=True)
    image = models.ImageField(upload_to='Userprofile', blank=True)
    date  = models.DateField(auto_now_add=True)

    def __str__(self):
    	return '%s %s' % (self.id,self.mobile)


def createProfile(sender, **kwargs):
	if kwargs['created']:
		user_profile = Userprofile.objects.created(user=kwargs['instance'])
		post_save.connect(createProfile, sender=User)  

