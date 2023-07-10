from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost


# Create your views here.

@login_required(login_url="signin")
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    posts = Post.objects.all()
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


def upload(request):
    if request.method == "POST":
        user = request.user
        profile = Profile.objects.get(user=user)
        image = request.FILES.get("image_upload")
        caption = request.POST["caption"]
        new_post = Post.objects.create(user_profile=profile, image=image, caption=caption)
        new_post.save()
    return redirect("/")


@login_required(login_url="signin")
def like_post(request):
    username = request.user.username
    post_id = request.GET.get("post_id")
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter is None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1

    else:
        post.no_of_likes -= 1
        like_filter.delete()
    post.save()
    return redirect("/")


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


