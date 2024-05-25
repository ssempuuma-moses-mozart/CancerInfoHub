
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("n/index", views.index, name="index"),
    path("n/login", views.login_view, name="login"),
    path("n/signin/", views.signin_view, name="signin"),
    path("n/signin/<int:item_id>/", views.signin_view, name="signin"),
    path("n/signup/", views.signup_view, name="signup"),
    path("n/signup/<int:item_id>/", views.signup_view, name="signup"),
    path("n/my_donations/<int:item_id>/", views.my_donations_view, name="my_donations"),
    path("n/dashboad/<int:item_id>/", views.dashboad_view, name="dashboad"),
    path("n/user_profile/<int:item_id>/", views.user_profile, name="user_profile"),
    path("n/logout", views.logout_view, name="logout"),
    path("n/user_logout", views.user_logout_view, name="user_logout"),
    path("n/register", views.register, name="register"),
    path("<str:username>", views.profile, name='profile'),
    path("n/following", views.following, name='following'),
    path("n/saved", views.saved, name="saved"),
    path("n/group", views.group, name="group"),
     path("n/chat_online", views.chat_online, name="chat_online"),
    path("n/createpost", views.create_post, name="createpost"),
    path("n/post/<int:id>/like", views.like_post, name="likepost"),
    path("n/post/<int:id>/unlike", views.unlike_post, name="unlikepost"),
    path("n/post/<int:id>/save", views.save_post, name="savepost"),
    path("n/post/<int:id>/unsave", views.unsave_post, name="unsavepost"),
    path("n/post/<int:post_id>/comments", views.comment, name="comments"),
    path("n/post/<int:post_id>/write_comment",views.comment, name="writecomment"),
    path("n/post/<int:post_id>/delete", views.delete_post, name="deletepost"),
    path("<str:username>/follow", views.follow, name="followuser"),
    path("<str:username>/unfollow", views.unfollow, name="unfollowuser"),
    path("n/post/<int:post_id>/edit", views.edit_post, name="editpost")
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

