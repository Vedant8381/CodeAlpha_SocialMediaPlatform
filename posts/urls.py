from django.urls import path
from . import views


urlpatterns = [

    # HOME
    path(
        "",
        views.home,
        name="home"
    ),

    # CREATE POST
    path(
        "create/",
        views.create_post,
        name="create_post"
    ),

    # LIKE / UNLIKE POST
    path(
        "like/<int:post_id>/",
        views.like_post,
        name="like_post"
    ),

    # ADD COMMENT
    path(
        "comment/<int:post_id>/",
        views.add_comment,
        name="add_comment"
    ),

    # EDIT POST
    path(
        "edit/<int:post_id>/",
        views.edit_post,
        name="edit_post"
    ),

    # DELETE POST
    path(
        "delete/<int:post_id>/",
        views.delete_post,
        name="delete_post"
    ),

    # FOLLOW / UNFOLLOW USER
    path(
        "follow/<int:user_id>/",
        views.follow_user,
        name="follow_user"
    ),

    # NOTIFICATIONS
    path(
        "notifications/",
        views.notifications,
        name="notifications"
    ),

]