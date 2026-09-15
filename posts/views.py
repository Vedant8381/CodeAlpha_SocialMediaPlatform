from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import (
    Post,
    Like,
    Comment,
    Follow,
    Notification
)


# ==========================================
# HOME
# ==========================================

def home(request):

    posts = Post.objects.all().order_by("-created_at")

    following_ids = []
    unread_notifications = 0

    if request.user.is_authenticated:

        following_ids = list(
            Follow.objects.filter(
                follower=request.user
            ).values_list(
                "following_id",
                flat=True
            )
        )

        unread_notifications = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()

    return render(
        request,
        "posts/home.html",
        {
            "posts": posts,
            "following_ids": following_ids,
            "unread_notifications": unread_notifications,
        }
    )


# ==========================================
# CREATE POST
# ==========================================

@login_required
def create_post(request):

    if request.method == "POST":

        content = request.POST.get(
            "content",
            ""
        ).strip()

        if content:

            Post.objects.create(
                user=request.user,
                content=content
            )

    return redirect("home")


# ==========================================
# LIKE / UNLIKE POST
# ==========================================

@login_required
def like_post(request, post_id):

    post = Post.objects.get(
        id=post_id
    )

    like = Like.objects.filter(
        user=request.user,
        post=post
    ).first()

    if like:

        # Already liked → Unlike
        like.delete()

    else:

        # Like post
        Like.objects.create(
            user=request.user,
            post=post
        )

        # Create like notification
        if post.user != request.user:

            Notification.objects.create(
                recipient=post.user,
                sender=request.user,
                notification_type="like",
                post=post,
                message=(
                    f"{request.user.username} "
                    f"liked your post."
                )
            )

    return redirect("home")


# ==========================================
# ADD COMMENT
# ==========================================

@login_required
def add_comment(request, post_id):

    if request.method == "POST":

        post = Post.objects.get(
            id=post_id
        )

        text = request.POST.get(
            "text",
            ""
        ).strip()

        if text:

            Comment.objects.create(
                user=request.user,
                post=post,
                text=text
            )

            # Create comment notification
            if post.user != request.user:

                Notification.objects.create(
                    recipient=post.user,
                    sender=request.user,
                    notification_type="comment",
                    post=post,
                    message=(
                        f"{request.user.username} "
                        f"commented on your post."
                    )
                )

    return redirect("home")


# ==========================================
# EDIT POST
# ==========================================

@login_required
def edit_post(request, post_id):

    post = Post.objects.get(
        id=post_id
    )

    # Only post owner can edit
    if post.user != request.user:

        return redirect("home")

    if request.method == "POST":

        content = request.POST.get(
            "content",
            ""
        ).strip()

        if content:

            post.content = content
            post.save()

            return redirect("home")

    return render(
        request,
        "posts/edit_post.html",
        {
            "post": post
        }
    )


# ==========================================
# DELETE POST
# ==========================================

@login_required
def delete_post(request, post_id):

    post = Post.objects.get(
        id=post_id
    )

    # Only post owner can delete
    if post.user != request.user:

        return redirect("home")

    if request.method == "POST":

        post.delete()

    return redirect("home")


# ==========================================
# FOLLOW / UNFOLLOW USER
# ==========================================

@login_required
def follow_user(request, user_id):

    target_user = User.objects.get(
        id=user_id
    )

    # Cannot follow yourself
    if target_user == request.user:

        return redirect("home")

    follow = Follow.objects.filter(
        follower=request.user,
        following=target_user
    ).first()

    if follow:

        # Already following → Unfollow
        follow.delete()

    else:

        # Create follow relationship
        Follow.objects.create(
            follower=request.user,
            following=target_user
        )

        # Create follow notification
        Notification.objects.create(
            recipient=target_user,
            sender=request.user,
            notification_type="follow",
            message=(
                f"{request.user.username} "
                f"started following you."
            )
        )

    return redirect("home")


# ==========================================
# NOTIFICATIONS
# ==========================================

@login_required
def notifications(request):

    notification_list = Notification.objects.filter(
        recipient=request.user
    ).order_by("-created_at")

    # Mark all notifications as read
    Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(
        is_read=True
    )

    return render(
        request,
        "posts/notifications.html",
        {
            "notifications": notification_list
        }
    )