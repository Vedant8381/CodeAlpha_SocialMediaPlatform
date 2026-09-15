from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from posts.models import Comment, Like, Post, Follow


# ==========================================
# REGISTER
# ==========================================

def register(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        # Check required fields
        if not username or not password or not confirm_password:

            messages.error(
                request,
                "Please fill all required fields."
            )

            return redirect("register")

        # Check username
        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("register")

        # Check password
        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect("register")

        # Create user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Registration successful! Please login."
        )

        return redirect("login")

    return render(
        request,
        "accounts/register.html"
    )


# ==========================================
# LOGIN
# ==========================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect("home")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

            return redirect("login")

    return render(
        request,
        "accounts/login.html"
    )


# ==========================================
# LOGOUT
# ==========================================

@login_required
def logout_view(request):

    logout(request)

    return redirect("home")


# ==========================================
# MY PROFILE
# ==========================================

@login_required
def profile(request):

    user_posts = Post.objects.filter(
        user=request.user
    ).order_by("-created_at")

    # Total likes received on user's posts
    total_likes = Like.objects.filter(
        post__user=request.user
    ).count()

    # Total comments received on user's posts
    total_comments = Comment.objects.filter(
        post__user=request.user
    ).count()

    # Total activities
    total_activities = (
        total_likes +
        total_comments
    )

    # Followers count
    followers_count = Follow.objects.filter(
        following=request.user
    ).count()

    # Following count
    following_count = Follow.objects.filter(
        follower=request.user
    ).count()

    return render(
        request,
        "accounts/profile.html",
        {
            "user_posts": user_posts,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_activities": total_activities,
            "followers_count": followers_count,
            "following_count": following_count,
        }
    )


# ==========================================
# FOLLOWERS LIST
# ==========================================

@login_required
def followers_list(request):

    followers = User.objects.filter(
        followers__follower=request.user
    ).distinct()

    return render(
        request,
        "accounts/followers.html",
        {
            "followers": followers
        }
    )


# ==========================================
# FOLLOWING LIST
# ==========================================

@login_required
def following_list(request):

    following = User.objects.filter(
        following__following=request.user
    ).distinct()

    return render(
        request,
        "accounts/following.html",
        {
            "following": following
        }
    )


# ==========================================
# OTHER USER PROFILE
# ==========================================

@login_required
def user_profile(request, user_id):

    profile_user = User.objects.get(
        id=user_id
    )

    user_posts = Post.objects.filter(
        user=profile_user
    ).order_by("-created_at")

    # Followers count
    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    # Following count
    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    # Check whether current user follows this user
    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    return render(
        request,
        "accounts/user_profile.html",
        {
            "profile_user": profile_user,
            "user_posts": user_posts,
            "followers_count": followers_count,
            "following_count": following_count,
            "is_following": is_following,
        }
    )


# ==========================================
# EDIT PROFILE
# ==========================================

@login_required
def edit_profile(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        # Username required
        if not username:

            messages.error(
                request,
                "Username cannot be empty."
            )

            return redirect("edit_profile")

        # Check username availability
        if User.objects.filter(
            username=username
        ).exclude(
            id=request.user.id
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("edit_profile")

        # Update profile
        request.user.username = username
        request.user.email = email

        request.user.save()

        messages.success(
            request,
            "Profile updated successfully!"
        )

        return redirect("profile")

    return render(
        request,
        "accounts/edit_profile.html"
    )
# ==========================================
# SEARCH USERS
# ==========================================

@login_required
def search_users(request):

    query = request.GET.get(
        "q",
        ""
    ).strip()

    users = User.objects.none()

    if query:

        users = User.objects.filter(
            username__icontains=query
        ).exclude(
            id=request.user.id
        ).order_by(
            "username"
        )

    return render(
        request,
        "accounts/search_users.html",
        {
            "query": query,
            "users": users,
        }
    )