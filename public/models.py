from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group, User
from django.urls import reverse
from cancer.models import *
from django.core.validators import MinLengthValidator


class CancerUnit(models.Model):
	name = models.CharField(max_length=250, blank=True, null=True,)
	category = models.CharField(max_length=250, blank=True, null=True,)
	location = models.CharField(max_length=250, blank=True, null=True,)
	description = models.CharField(max_length=800,blank=True, null=True,)
	uploaded_image = models.ImageField(upload_to='uploaded_image/', blank=True, null=True,)
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.name} {self.name}'
	
class CancerExpert(models.Model):
	name = models.CharField(max_length=250, blank=True, null=True,)
	speciality = models.CharField(max_length=250, blank=True, null=True,)
	location = models.CharField(max_length=250, blank=True, null=True,)
	description = models.CharField(max_length=250,blank=True, null=True,)
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.name} {self.name}'	
	

class CancerNetwork(models.Model):
	name = models.CharField(max_length=250, blank=True, null=True,)
	category = models.CharField(max_length=250, blank=True, null=True,)
	location = models.CharField(max_length=250, blank=True, null=True,)
	description = models.CharField(max_length=800,blank=True, null=True,)
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.name} {self.name}'
	
class CancerOrganization(models.Model):
	name = models.CharField(max_length=250, blank=True, null=True,)
	category = models.CharField(max_length=250, blank=True, null=True,)
	location = models.CharField(max_length=250, blank=True, null=True,)
	description = models.CharField(max_length=800,blank=True, null=True,)
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.name} {self.name}'	


class Video(models.Model):
	video_file = models.FileField(upload_to='videos/', blank=True, null=True,) 
	title = models.CharField(max_length=250, blank=True, null=True,)
	description = models.CharField(max_length=800, blank=True, null=True,)
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.title} {self.title}'
	
class Presentation(models.Model):
	name = models.CharField(max_length=250)
	organization = models.CharField(max_length=250, blank=True, null=True,)
	profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True,)
	topic = models.CharField(max_length=250, blank=True, null=True,)
	powerpoint_file = models.FileField(upload_to='powerpoint_files/', blank=True, null=True,)
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.name} {self.name}'



class CancerType(models.Model):
	title = models.CharField(max_length=250, blank=True, null=True,)
	description = models.CharField(max_length=250, blank=True, null=True,)
	cancertype = models.CharField(max_length=250, blank=True, null=True,)
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.title} {self.cancertype}'
	

class Crowdfunding(models.Model):
    campaign_image = models.ImageField(upload_to='campaign_images/', blank=True, null=True,)
    title = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    raised_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    open_date = models.DateField(default=timezone.now)
    closing_date = models.DateField(blank=True, null=True)
    def __str__(self):
	    return f'{self.title} {self.title}'

class Donation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Crowdfunding, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2)
    date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return f"Donation by {self.user} for {self.item} on {self.date}"

