from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from team_finder.constants import DEFAULT_PAGE_SIZE
from team_finder.pagination import paginate_queryset

from .forms import LoginForm, ProfileEditForm, RegisterForm, UserPasswordChangeForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect("projects:project_list")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("users:login")

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("projects:project_list")

    form = LoginForm(request.POST or None, request=request)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("projects:project_list")

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("projects:project_list")


def user_detail(request, user_id):
    profile_user = get_object_or_404(User.objects.prefetch_related("owned_projects"), pk=user_id)
    return render(request, "users/user-details.html", {"user": profile_user})


@login_required
def edit_profile(request):
    form = ProfileEditForm(request.POST or None, request.FILES or None, instance=request.user)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("users:user_detail", user_id=request.user.id)

    return render(request, "users/edit_profile.html", {"form": form, "user": request.user})


def participants_list(request):
    participants_qs = User.objects.all().order_by("-date_joined")
    page_obj = paginate_queryset(request, participants_qs, per_page=DEFAULT_PAGE_SIZE)

    context = {
        "participants": page_obj.object_list,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
    }
    return render(request, "users/participants.html", context)


@login_required
def change_password(request):
    form = UserPasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect("users:user_detail", user_id=request.user.id)

    return render(request, "users/change_password.html", {"form": form})
