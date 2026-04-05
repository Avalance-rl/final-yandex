import json
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from team_finder.constants import DEFAULT_PAGE_SIZE, SKILL_SUGGESTIONS_LIMIT
from team_finder.pagination import paginate_queryset

from .forms import ProjectForm
from .models import Project, Skill


def project_list(request):
    projects_qs = Project.objects.select_related("owner").prefetch_related("participants", "skills")

    active_skill = request.GET.get("skill", "").strip()
    if active_skill:
        projects_qs = projects_qs.filter(skills__name__iexact=active_skill).distinct()

    page_obj = paginate_queryset(request, projects_qs, per_page=DEFAULT_PAGE_SIZE)

    context = {
        "projects": page_obj.object_list,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "all_skills": list(Skill.objects.order_by("name").values_list("name", flat=True)),
        "active_skill": active_skill,
    }
    return render(request, "projects/project_list.html", context)


def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("skills", "participants"),
        pk=project_id,
    )
    return render(request, "projects/project-details.html", {"project": project})


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        form.save_skills(project)
        return redirect("projects:project_detail", project_id=project.id)

    return render(request, "projects/create-project.html", {"form": form, "is_edit": False})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id != request.user.id:
        return redirect("projects:project_detail", project_id=project.id)

    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        form.save_skills(project)
        return redirect("projects:project_detail", project_id=project.id)

    return render(request, "projects/create-project.html", {"form": form, "is_edit": True})


@login_required
@require_POST
def complete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id != request.user.id:
        return JsonResponse({"status": "error", "message": "forbidden"}, status=HTTPStatus.FORBIDDEN)

    project.status = Project.STATUS_CLOSED
    project.save(update_fields=["status"])
    return JsonResponse({"status": "ok"})


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id == request.user.id:
        return JsonResponse(
            {"status": "error", "message": "owner cannot participate"},
            status=HTTPStatus.BAD_REQUEST,
        )

    if project.participants.filter(pk=request.user.id).exists():
        project.participants.remove(request.user)
        participant = False
    else:
        project.participants.add(request.user)
        participant = True

    return JsonResponse({"status": "ok", "participant": participant})


@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.favorites.filter(pk=request.user.id).exists():
        project.favorites.remove(request.user)
        favorite = False
    else:
        project.favorites.add(request.user)
        favorite = True
    return JsonResponse({"status": "ok", "favorite": favorite})


@login_required
def favorite_projects(request):
    projects_qs = request.user.favorites.select_related("owner").prefetch_related("participants")
    page_obj = paginate_queryset(request, projects_qs, per_page=DEFAULT_PAGE_SIZE)

    context = {
        "projects": page_obj.object_list,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
    }
    return render(request, "projects/favorite_projects.html", context)


@require_GET
def skill_suggestions(request):
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse([], safe=False)

    skills = Skill.objects.filter(name__icontains=q).order_by("name")[:SKILL_SUGGESTIONS_LIMIT]
    return JsonResponse([{"id": skill.id, "name": skill.name} for skill in skills], safe=False)


@login_required
@require_POST
def add_project_skill(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id != request.user.id:
        return JsonResponse({"detail": "forbidden"}, status=HTTPStatus.FORBIDDEN)

    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    skill = None
    skill_id = payload.get("skill_id")
    if skill_id:
        skill = Skill.objects.filter(pk=skill_id).first()
        if skill is None:
            return JsonResponse({"detail": "skill not found"}, status=HTTPStatus.NOT_FOUND)

    if skill is None:
        raw_name = (payload.get("name") or "").strip()
        if not raw_name:
            return JsonResponse({"detail": "name is required"}, status=HTTPStatus.BAD_REQUEST)

        existing = Skill.objects.filter(name__iexact=raw_name).first()
        if existing:
            skill = existing
        else:
            skill = Skill.objects.create(name=raw_name)

    project.skills.add(skill)
    return JsonResponse({"id": skill.id, "name": skill.name})


@login_required
@require_POST
def remove_project_skill(request, project_id, skill_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id != request.user.id:
        return JsonResponse({"detail": "forbidden"}, status=HTTPStatus.FORBIDDEN)

    skill = get_object_or_404(Skill, pk=skill_id)
    project.skills.remove(skill)
    return JsonResponse({"status": "ok"})
