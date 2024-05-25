from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import json

from public.models import Crowdfunding, Donation
from public.views import crowdfunding

from .models import *


def index(request):
    all_posts = Post.objects.all().order_by('-date_created')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    followings = []
    suggestions = []
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
    return render(request, "network/index.html", {
        "posts": posts,
        "suggestions": suggestions,
        "page": "all_posts",
        'profile': False
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        profile = request.FILES.get("profile")
        print(f"--------------------------Profile: {profile}----------------------------")
        cover = request.FILES.get('cover')
        print(f"--------------------------Cover: {cover}----------------------------")

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            if profile is not None:
                user.profile_pic = profile
            else:
                user.profile_pic = "profile_pic/no_pic.png"
            user.cover = cover           
            user.save()
            Follower.objects.create(user=user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

def profile(request, username):
    try:
        user = User.objects.get(username=username)
        all_posts = Post.objects.filter(creater=user).order_by('-date_created')
        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        if page_number is None:
            page_number = 1
        posts = paginator.get_page(page_number)
        followings = []
        suggestions = []
        follower = False
        if request.user.is_authenticated:
            followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
            suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]

            try:
                follower_instance = Follower.objects.get(user=user)
                follower_count = follower_instance.followers.all().count()
                follower = request.user in follower_instance.followers.all()
            except Follower.DoesNotExist:
                follower_count = 0
                follower = False

        else:
            follower_count = 0  # Set follower_count to 0 if user is not authenticated

        following_count = Follower.objects.filter(followers=user).count()
        return render(request, 'network/profile.html', {
            "username": user,
            "posts": posts,
            "posts_count": all_posts.count(),
            "suggestions": suggestions,
            "page": "profile",
            "is_follower": follower,
            "follower_count": follower_count,
            "following_count": following_count
        })
    except User.DoesNotExist:
        return HttpResponseNotFound("User does not exist.")

def following(request):
    if request.user.is_authenticated:
        following_user = Follower.objects.filter(followers=request.user).values('user')
        all_posts = Post.objects.filter(creater__in=following_user).order_by('-date_created')
        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        if page_number == None:
            page_number = 1
        posts = paginator.get_page(page_number)
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        return render(request, "network/index.html", {
            "posts": posts,
            "suggestions": suggestions,
            "page": "following"
        })
    else:
        return HttpResponseRedirect(reverse('login'))

def saved(request):
    if request.user.is_authenticated:
        all_posts = Post.objects.filter(savers=request.user).order_by('-date_created')

        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        if page_number == None:
            page_number = 1
        posts = paginator.get_page(page_number)

        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        return render(request, "network/index.html", {
            "posts": posts,
            "suggestions": suggestions,
            "page": "saved"
        })
    else:
        return HttpResponseRedirect(reverse('login'))
    

def chat_online(request):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            user = User.objects.all
            print(f".....................User: {user}......................")
            print(f".....................Follower: {request.user}......................")
            try:
                (follower, create) = Follower.objects.get_or_create(user=user)
                follower.followers.add(request.user)
                follower.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
           return render(request, "network/index.html")
    else:
        return HttpResponseRedirect(reverse('login'))
   


@login_required
def create_post(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        pic = request.FILES.get('picture')
        try:
            post = Post.objects.create(creater=request.user, content_text=text, content_image=pic)
            return HttpResponseRedirect(reverse('index'))
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Method must be 'POST'")

@login_required
@csrf_exempt
def edit_post(request, post_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        pic = request.FILES.get('picture')
        img_chg = request.POST.get('img_change')
        post_id = request.POST.get('id')
        post = Post.objects.get(id=post_id)
        try:
            post.content_text = text
            if img_chg != 'false':
                post.content_image = pic
            post.save()
            
            if(post.content_text):
                post_text = post.content_text
            else:
                post_text = False
            if(post.content_image):
                post_image = post.img_url()
            else:
                post_image = False
            
            return JsonResponse({
                "success": True,
                "text": post_text,
                "picture": post_image
            })
        except Exception as e:
            print('-----------------------------------------------')
            print(e)
            print('-----------------------------------------------')
            return JsonResponse({
                "success": False
            })
    else:
            return HttpResponse("Method must be 'POST'")

@csrf_exempt
def like_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            print(post)
            try:
                post.likers.add(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def unlike_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            print(post)
            try:
                post.likers.remove(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def save_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            print(post)
            try:
                post.savers.add(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def unsave_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            print(post)
            try:
                post.savers.remove(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def follow(request, username):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            user = User.objects.get(username=username)
            print(f".....................User: {user}......................")
            print(f".....................Follower: {request.user}......................")
            try:
                (follower, create) = Follower.objects.get_or_create(user=user)
                follower.followers.add(request.user)
                follower.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def unfollow(request, username):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            user = User.objects.get(username=username)
            print(f".....................User: {user}......................")
            print(f".....................Unfollower: {request.user}......................")
            try:
                follower = Follower.objects.get(user=user)
                follower.followers.remove(request.user)
                follower.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def comment(request, post_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body)
            comment = data.get('comment_text')
            post = Post.objects.get(id=post_id)
            try:
                newcomment = Comment.objects.create(post=post,commenter=request.user,comment_content=comment)
                post.comment_count += 1
                post.save()
                print(newcomment.serialize())
                return JsonResponse([newcomment.serialize()], safe=False, status=201)
            except Exception as e:
                return HttpResponse(e)
    
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post)
        comments = comments.order_by('-comment_time').all()
        return JsonResponse([comment.serialize() for comment in comments], safe=False)
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def delete_post(request, post_id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(id=post_id)
            if request.user == post.creater:
                try:
                    delet = post.delete()
                    return HttpResponse(status=201)
                except Exception as e:
                    return HttpResponse(e)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))



# def signin_view(request):
  
#     if request.method == "POST":


#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password)

       
#         if user is not None:
#             login(request, user)
           
#             return redirect('dashboad')
#         else:
#             return render(request, "network/signin.html", {
#                 "message": "Invalid username and/or password."
#             })
#     else:
#         return render(request, "network/signin.html")


def signin_view(request, item_id=None):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if item_id is not None:
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
                return render(request, 'network/dashboad.html', context)
            else:
                return redirect('dashboad')  # Redirect to dashboard if no item_id is provided
        else:
            return render(request, "network/signin.html", {
                "message": "Invalid username and/or password."
            })
    else:
        # return render(request, "network/signin.html")
        return render(request, 'network/signin.html', {'item_id': item_id})

    

def signup_view(request, item_id=None):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        profile = request.FILES.get("profile")
        print(f"--------------------------Profile: {profile}----------------------------")
        cover = request.FILES.get('cover')
        print(f"--------------------------Cover: {cover}----------------------------")

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            if profile is not None:
                user.profile_pic = profile
            else:
                user.profile_pic = "profile_pic/no_pic.png"
            user.cover = cover           
            user.save()
            Follower.objects.create(user=user)
        except IntegrityError:
            return render(request, "network/signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        if item_id is not None:
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
            return render(request, 'network/dashboad.html', context)
        else:
            return HttpResponseRedirect(reverse("dashboad"))
    else:
        return render(request, "network/signup.html", {'item_id': item_id})

# def signup_view(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         email = request.POST["email"]
#         fname = request.POST["firstname"]
#         lname = request.POST["lastname"]
#         profile = request.FILES.get("profile")
#         print(f"--------------------------Profile: {profile}----------------------------")
#         cover = request.FILES.get('cover')
#         print(f"--------------------------Cover: {cover}----------------------------")

      
#         password = request.POST["password"]
#         confirmation = request.POST["confirmation"]
#         if password != confirmation:
#             return render(request, "network/register.html", {
#                 "message": "Passwords must match."
#             })

        
#         try:
#             user = User.objects.create_user(username, email, password)
#             user.first_name = fname
#             user.last_name = lname
#             if profile is not None:
#                 user.profile_pic = profile
#             else:
#                 user.profile_pic = "profile_pic/no_pic.png"
#             user.cover = cover           
#             user.save()
#             Follower.objects.create(user=user)
#         except IntegrityError:
#             return render(request, "network/signup.html", {
#                 "message": "Username already taken."
#             })
#         login(request, user)
#         return HttpResponseRedirect(reverse("index"))
#     else:
#         return render(request, "network/signup.html")   
    

# def dashboad_view(request):
    
#     return HttpResponseRedirect(reverse("dashboad")) 

# @login_required
# @csrf_exempt
# def dashboad_view(request):
 
# 	context = {}
	
# 	return render(request, 'network/dashboad.html', context) 



# def dashboad_view(request, item_id):
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

#     return render(request, 'network/dashboad.html', context)


@login_required
@csrf_exempt
def dashboad_view(request, item_id):
    item = get_object_or_404(Crowdfunding, pk=item_id)

    # Get all donations related to the item
    # donations = Donation.objects.filter(item=item)
    
    # Filter donations related to the item by the current logged-in user
    donations = Donation.objects.filter(item=item, user=request.user)

    posts = Post.objects.all().order_by('-date_created')
    # Assuming you have a queryset of crowdfunding items
    crowdfunding = Crowdfunding.objects.all()

    # Pass user details to the context
    user = request.user

    # Calculate total donation amount for the current user
    total_donation = Donation.objects.filter(user=request.user).aggregate(models.Sum('amount'))['amount__sum']
     # Set total donation amount to 0 if it's None
    total_donation = total_donation if total_donation is not None else 0

    context = {
        'campaign_image': item.campaign_image,
        'title': item.title,
        'description': item.description,
        'name': item.name,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,
        'item_id': item_id,
        'crowdfunding': crowdfunding,
        'closing_date': item.closing_date,
        "posts": posts,
        'donations': donations,  # Pass donations to the context
        'user': user,  # Pass user details to the context
        'total_donation': total_donation  # Pass total donation amount to the context
    }

    return render(request, 'network/dashboad.html', context)


@login_required
@csrf_exempt
def my_donations_view(request, item_id):
    item = get_object_or_404(Crowdfunding, pk=item_id)

    donations = Donation.objects.filter(item=item, user=request.user)
    crowdfunding = Crowdfunding.objects.all()
    user = request.user
    total_donation = Donation.objects.filter(user=request.user).aggregate(models.Sum('amount'))['amount__sum']
     # Set total donation amount to 0 if it's None
    total_donation = total_donation if total_donation is not None else 0

    context = {
        'campaign_image': item.campaign_image,
        'title': item.title,
        'description': item.description,
        'name': item.name,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,
        'item_id': item_id,
        'crowdfunding': crowdfunding,
        'closing_date': item.closing_date,
        'donations': donations,  # Pass donations to the context
        'user': user,  # Pass user details to the context
        'total_donation': total_donation  # Pass total donation amount to the context
    }

    return render(request, 'network/my_donations.html', context)


def user_logout_view(request):
    logout(request)
    return render(request, 'public/home.html')     



def user_profile(request, item_id):
    item = get_object_or_404(Crowdfunding, pk=item_id)

    # Get all donations related to the item
    # donations = Donation.objects.filter(item=item)
    
    # Filter donations related to the item by the current logged-in user
    donations = Donation.objects.filter(item=item, user=request.user)

    # Pass user details to the context
    user = request.user

    # Calculate total donation amount for the current user
    total_donation = Donation.objects.filter(user=request.user).aggregate(models.Sum('amount'))['amount__sum']
     # Set total donation amount to 0 if it's None
    total_donation = total_donation if total_donation is not None else 0

    context = {
        'campaign_image': item.campaign_image,
        'title': item.title,
        'description': item.description,
        'name': item.name,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,
        'item_id': item_id,
        'closing_date': item.closing_date,
        'donations': donations,  # Pass donations to the context
        'user': user,  # Pass user details to the context
        'total_donation': total_donation  # Pass total donation amount to the context
    }

    return render(request, 'network/user_profile.html', context)


def group(request):
    if request.user.is_authenticated:
        all_posts = Post.objects.filter(savers=request.user).order_by('-date_created')

        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        if page_number == None:
            page_number = 1
        posts = paginator.get_page(page_number)

        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        return render(request, "network/index.html", {
            "posts": posts,
            "suggestions": suggestions,
            "page": "saved"
        })
    else:
        return HttpResponseRedirect(reverse('login'))  
    
