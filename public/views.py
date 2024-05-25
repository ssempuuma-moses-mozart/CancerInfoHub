from django.shortcuts import render, redirect
from cancer.models import *
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser

from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	CreateView
	)
from django.db import IntegrityError
from django.db.models import Sum, Count

def home(request):
	# cancer_units = unit.objects.all().order_by('name')
	context = {}

	return render(request, 'public/home.html', context)


def cancer_units(request):
    # Fetch all CancerUnit objects from the database
    cancer_units = CancerUnit.objects.all()

    if request.method == 'POST':
        form = CancerUnitCreateForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = CancerUnitCreateForm()
    
    context = {
        'form': form,
        'cancer_units': cancer_units,  # Pass the queryset to the template context
    }
    return render(request, 'public/cancer_units.html', context)

def cancer_experts(request):
    # Fetch all CancerExpert objects from the database
    cancer_experts = CancerExpert.objects.all()

    if request.method == 'POST':
        form = CancerExpertCreateForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = CancerExpertCreateForm()
    
    context = {
        'form': form,
        'cancer_experts': cancer_experts,  # Pass the queryset to the template context
    }
    return render(request, 'public/cancer_experts.html', context)



def cancer_networks(request):
    # Fetch all CancerUnit objects from the database
    cancer_networks = CancerNetwork.objects.all()

    if request.method == 'POST':
        form = CancerNetworkCreateForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = CancerNetworkCreateForm()
    
    context = {
        'form': form,
        'cancer_networks': cancer_networks,  # Pass the queryset to the template context
    }
    return render(request, 'public/cancer_networks.html', context)


def cancer_organizations(request):
    # Fetch all CancerUnit objects from the database
    cancer_organizations = CancerOrganization.objects.all()

    if request.method == 'POST':
        form = CancerOrganizationCreateForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = CancerOrganizationCreateForm()
    
    context = {
        'form': form,
        'cancer_organizations': cancer_organizations,  # Pass the queryset to the template context
    }
    return render(request, 'public/cancer_organizations.html', context)

# def cancer_experts(request):
	
# 	context = {}
	
# 	return render(request, 'public/cancer_experts.html', context)

def video(request):
    # Fetch all Video objects from the database
    video = Video.objects.all()

    if request.method == 'POST':
        form = VideoCreateForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = VideoCreateForm()
    
    context = {
        'form': form,
        'video': video,  # Pass the queryset to the template context
    }
    return render(request, 'public/video.html', context)


def presentation(request):
    # Fetch all Video objects from the database
    presentation = Presentation.objects.all()

    if request.method == 'POST':
        form = PresentationCreateForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = PresentationCreateForm()
    
    context = {
        'form': form,
        'presentation': presentation,  # Pass the queryset to the template context
    }
    return render(request, 'public/presentation.html', context)


def cancer_experts_info(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(CancerExpert, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'name': item.name,
        'location': item.location,
        'speciality': item.speciality,
        'description': item.description
    }
    
    # Render the details page template with the item details
    return render(request, 'public/cancer_experts_info.html', context)


# def cancer_experts_info(request):
	
# 	context = {}
	
# 	return render(request, 'public/cancer_experts_info.html', context)


def cancer_units_info(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(CancerUnit, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'name': item.name,
        'category': item.category,
        'location': item.location,
        'uploaded_image': item.uploaded_image,
        'description': item.description
    }
    
    # Render the details page template with the item details
    return render(request, 'public/cancer_units_info.html', context)


def cancer_types_info(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(CancerType, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'title': item.title,
        'description': item.description,
        'cancertype': item.cancertype,
    }
    
    # Render the details page template with the item details
    return render(request, 'public/cancer_types_info.html', context)


def cancer_organizations_info(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(CancerOrganization, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'name': item.name,
        'category': item.category,
        'location': item.location,
        'description': item.description
    }
    
    # Render the details page template with the item details
    return render(request, 'public/cancer_organizations_info.html', context)

def cancer_networks_info(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(CancerNetwork, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'name': item.name,
        'category': item.category,
        'location': item.location,
        'description': item.description
    }
    
    # Render the details page template with the item details
    return render(request, 'public/cancer_networks_info.html', context)


def cancer_types(request):
    # Fetch all CancerUnit objects from the database
    cancer_types = CancerType.objects.all()

    if request.method == 'POST':
        form = CancerTypeCreateForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = CancerTypeCreateForm()
    
    context = {
        'form': form,
        'cancer_types': cancer_types,  # Pass the queryset to the template context
    }
    return render(request, 'public/cancer_types.html', context)

def infographics(request):
	# cancer_units = unit.objects.all().order_by('name')
	context = {}
	
	return render(request, 'public/infographics.html', context)

def presentations(request):
	# cancer_units = unit.objects.all().order_by('name')
	context = {}
	
	return render(request, 'public/presentations.html', context)

def keynotes(request):
	# cancer_units = unit.objects.all().order_by('name')
	context = {}
	
	return render(request, 'public/keynotes.html', context)

def faqs(request):
	# cancer_units = unit.objects.all().order_by('name')
	context = {}
	
	return render(request, 'public/faqs.html', context)

# def crowdfunding(request):

# 	context = {}
	
# 	return render(request, 'public/crowdfunding.html', context)


def crowdfunding(request):
    crowdfunding = Crowdfunding.objects.all()

    for unit in crowdfunding:
        if unit.goal_amount != 0:
            unit.percentage_achieved = (unit.raised_amount / unit.goal_amount) * 100
        else:
            unit.percentage_achieved = 0

    if request.method == 'POST':
        form = CrowdfundingCreateForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = CrowdfundingCreateForm()
    
    context = {
        'form': form,
        'crowdfunding': crowdfunding,  # Pass the queryset to the template context
    }
    return render(request, 'public/crowdfunding.html', context)



# def crowdfunding(request):
    
#     crowdfunding = Crowdfunding.objects.all()

#     if request.method == 'POST':
#         form = CrowdfundingCreateForm(request.POST)
#         if form.is_valid():
#             form.save()  
#             return redirect('success_url') 
#     else:
#         form = CrowdfundingCreateForm()
    
#     context = {
#         'form': form,
#         'crowdfunding': crowdfunding, 
#     }
#     return render(request, 'public/crowdfunding.html', context)


def fundraiser(request):
	# cancer_units = unit.objects.all().order_by('name')
	context = {}
	
	return render(request, 'public/fundraiser.html', context)


def donate(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(Crowdfunding, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'campaign_image': item.campaign_image,
        'title': item.title,
        'description': item.description,
        'name': item.name,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,  # Pass the donation_id to the template context
        'closing_date': item.closing_date
        
    }
    
    # Render the details page template with the item details
    return render(request, 'public/donate.html', context)


def mobile_money(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(Crowdfunding, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'campaign_image': item.campaign_image,
        'title': item.title,
        'description': item.description,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,  # Pass the donation_id to the template context
        'closing_date': item.closing_date
    }
    
    # Render the details page template with the item details
    return render(request, 'public/mobile_money.html', context)



# @login_required
def pay(request, item_id):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        user = request.user
        item = get_object_or_404(Crowdfunding, pk=item_id)
        
        # Update raised_amount of the selected item
        item.raised_amount += int(amount)  # Convert amount to integer
        item.save()

        # Save the donation details
        donation = Donation(user=user, item=item, amount=amount)
        donation.save()

        # Return a JSON response indicating success
        return JsonResponse({'success': True})

    # If the request method is not POST, render the pay.html template as before
    item = get_object_or_404(Crowdfunding, pk=item_id)
    context = {
        'campaign_image': item.campaign_image,
        'title': item.title,
        'description': item.description,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,
        'closing_date': item.closing_date
    }

    # Check if the user is authenticated
    if isinstance(request.user, AnonymousUser):
        context['authenticated'] = False
    else:
        context['authenticated'] = True

    return render(request, 'public/pay.html', context)


# def pay(request, item_id):
   
#     item = get_object_or_404(Crowdfunding, pk=item_id)
    
   
#     context = {
#         'campaign_image': item.campaign_image,
#         'title': item.title,
#         'description': item.description,
#         'raised_amount': item.raised_amount,
#         'goal_amount': item.goal_amount,
#         'open_date': item.open_date,
#         'donation_id': item_id,  
#         'closing_date': item.closing_date
#     }
    
#     return render(request, 'public/pay.html', context)


def give_gift(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(Crowdfunding, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'campaign_image': item.campaign_image,
        'title': item.title,
        'description': item.description,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,  # Pass the donation_id to the template context
        'closing_date': item.closing_date
    }
    
    # Render the details page template with the item details
    return render(request, 'public/give_gift.html', context)

def pay_via_bank(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(Crowdfunding, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'campaign_image': item.campaign_image,
        'title': item.title,
        'description': item.description,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,  # Pass the donation_id to the template context
        'closing_date': item.closing_date
    }
    
    # Render the details page template with the item details
    return render(request, 'public/pay_via_bank.html', context)

def settings(request):
	return render(request, 'public/settings.html', {'title': 'Settings'})

def search_google(request):
	return render(request, 'public/search_google.html', {'title': 'Search'})

class SliderTemplate(TemplateView):
	template_name = 'public/slider.html'

class SliderMainTemplate(TemplateView):
	template_name = 'public/slider_main.html'
