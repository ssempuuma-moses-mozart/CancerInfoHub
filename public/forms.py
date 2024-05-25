from django import forms
from .models import *
import datetime

# class ApplyCreateForm(forms.ModelForm):
# 	class Meta:
# 		model = ServiceProvider
# 		fields =('service','name','capacity','phone','email','address','description')

class CancerUnitCreateForm(forms.ModelForm):
	class Meta:
		model = CancerUnit
		fields =('name','category','location','description','uploaded_image','date_created','date')

class CancerTypeCreateForm(forms.ModelForm):
	class Meta:
		model = CancerType
		fields =('title','description','cancertype','date_created','date')

class CancerExpertCreateForm(forms.ModelForm):
	class Meta:
		model = CancerExpert
		fields =('name','speciality','location','description','date_created','date')

class VideoCreateForm(forms.ModelForm):
	class Meta:
		model = Video
		fields =('video_file','title','description','date_created','date')

class PresentationCreateForm(forms.ModelForm):
	class Meta:
		model = Presentation
		fields =('name','organization','profile_image','topic','powerpoint_file','date_created','date')

class CancerNetworkCreateForm(forms.ModelForm):
	class Meta:
		model = CancerNetwork
		fields =('name','category','location','description','date_created','date')

class CancerOrganizationCreateForm(forms.ModelForm):
	class Meta:
		model = CancerOrganization
		fields =('name','category','location','description','date_created','date')

class CrowdfundingCreateForm(forms.ModelForm):
	class Meta:
		model = Crowdfunding
		fields =('campaign_image','title','description','name','raised_amount','goal_amount','open_date','closing_date')






