from django.urls import path
from . import views


urlpatterns = [

    # REGISTER
    path(
        "register/",
        views.register,
        name="register"
    ),

    # LOGIN
    path(
        "login/",
        views.login_view,
        name="login"
    ),

    # LOGOUT
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # MY PROFILE
    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    # EDIT PROFILE
    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_profile"
    ),

    # FOLLOWERS
    path(
        "profile/followers/",
        views.followers_list,
        name="followers"
    ),

    # FOLLOWING
    path(
        "profile/following/",
        views.following_list,
        name="following"
    ),

    # OTHER USER PROFILE
    path(
        "user/<int:user_id>/",
        views.user_profile,
        name="user_profile"
    ),

    # SEARCH USERS
    path(
        "search/",
        views.search_users,
        name="search_users"
    ),

]