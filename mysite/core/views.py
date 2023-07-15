import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount


# Create your views here.

@login_required(login_url="signin")
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    posts = []
    followings_users = FollowersCount.objects.filter(follower=request.user.username)
    for following in followings_users:
        posts += Post.objects.filter(username=following.user)
        print(following.user)
    return render(request, "index.html", {"user_profile": user_profile,
                                          "posts": posts
                                          })


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request, "Name or password is incorrect")
            return redirect("signin")
    else:
        return render(request, "signin.html")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "User with this email is exists")
                return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "User with this username is exists")
                return redirect("signup")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Log user in and redirect to settings page

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # Create a Profile object to the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect("settings")

        else:
            messages.info(request, "Passwords do not match")
            return redirect("signup")

    else:
        return render(request, "signup.html")


@login_required(login_url="signin")
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    if request.method == "POST":
        username = request.POST.get("username")
        username_profile_list = Profile.objects.filter(username=username)
    return render(request, "search.html", context={"user_profile": user_profile,
                                                   "username_profile_list": username_profile_list,
                                                   "username": username
                                                   })


def upload(request):
    if request.method == "POST":
        user = request.user
        username = request.user.username
        profile = Profile.objects.get(user=user)
        image = request.FILES.get("image_upload")
        caption = request.POST["caption"]
        new_post = Post.objects.create(user_profile=profile, image=image, caption=caption, username=username)
        new_post.save()
    return redirect("/")


@login_required(login_url="signin")
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user_profile=user_profile)
    user_posts_length = len(user_posts)
    num_of_followers = FollowersCount.objects.filter(user=pk)
    is_followed = FollowersCount.objects.filter(user=pk, follower=request.user.username).first()
    num_of_following = FollowersCount.objects.filter(follower=pk)

    follow_button_text = "Unfollow"
    if is_followed is None:
        follow_button_text = "Follow"

    return render(request, "profile.html", context={"user_profile": user_profile,
                                                    "user_object": user_object,
                                                    "user_posts": user_posts,
                                                    "user_posts_length": user_posts_length,
                                                    "num_of_followers": len(num_of_followers),
                                                    "follow_button_text": follow_button_text,
                                                    "num_of_following": len(num_of_following)
                                                    })


@login_required(login_url="signin")
def follow(request):
    if request.method == "POST":
        follower = request.POST.get("follower")
        user = request.POST.get("user")

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
        return redirect(f"/profile/{user}")
    else:
        return redirect("/")


@login_required(login_url="signin")
def like_post(request):
    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        data = json.loads(request.body)
        username = request.user.username
        post_id = data["post_id"]
        post = Post.objects.get(id=post_id)
        like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
        print(like_filter)
        if like_filter is None:
            new_like = LikePost.objects.create(post_id=post_id, username=username)
            new_like.save()
            post.no_of_likes += 1
        else:
            post.no_of_likes -= 1
            like_filter.delete()
        likes_count = post.no_of_likes
        post.save()
        return JsonResponse({"likes_count": likes_count})


@login_required(login_url="signin")
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        bio = request.POST["bio"]
        location = request.POST["location"]
        if request.FILES.get("image"):
            image = request.FILES.get("image")
            user_profile.profile_img = image

        user_profile.first_name = first_name.capitalize()
        user_profile.last_name = last_name.capitalize()
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        return redirect("settings")

    return render(request, "setting.html", {"user_profile": user_profile})


@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("signin")


