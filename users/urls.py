from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("register", views.register_view, name="register_without_slash"),
    path("register/", views.register_view, name="register"),
    path("login", views.login_view, name="login_without_slash"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout_without_slash"),
    path("logout/", views.logout_view, name="logout"),
    path("edit-profile", views.edit_profile, name="edit_profile_without_slash"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("list", views.participants_list, name="participants_list_without_slash"),
    path("list/", views.participants_list, name="participants_list"),
    path("change-password", views.change_password, name="change_password_without_slash"),
    path("change-password/", views.change_password, name="change_password"),
    path("<int:user_id>", views.user_detail, name="user_detail_without_slash"),
    path("<int:user_id>/", views.user_detail, name="user_detail"),
]
