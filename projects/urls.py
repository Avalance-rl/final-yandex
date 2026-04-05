from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("list", views.project_list, name="project_list_without_slash"),
    path("list/", views.project_list, name="project_list"),
    path("create-project", views.create_project, name="create_project_without_slash"),
    path("create-project/", views.create_project, name="create_project"),
    path("favorites/", views.favorite_projects, name="favorite_projects"),
    path("skills/", views.skill_suggestions, name="skill_suggestions"),
    path("<int:project_id>", views.project_detail, name="project_detail_without_slash"),
    path("<int:project_id>/", views.project_detail, name="project_detail"),
    path("<int:project_id>/edit", views.edit_project, name="edit_project_without_slash"),
    path("<int:project_id>/edit/", views.edit_project, name="edit_project"),
    path("<int:project_id>/complete/", views.complete_project, name="complete_project"),
    path("<int:project_id>/toggle-participate/", views.toggle_participate, name="toggle_participate"),
    path("<int:project_id>/toggle-favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("<int:project_id>/skills/add/", views.add_project_skill, name="add_project_skill"),
    path(
        "<int:project_id>/skills/<int:skill_id>/remove/",
        views.remove_project_skill,
        name="remove_project_skill",
    ),
]
