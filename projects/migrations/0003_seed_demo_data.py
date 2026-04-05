from django.db import migrations
from django.contrib.auth.hashers import make_password


DEMO_PASSWORD = "demo12345"

DEMO_USERS = [
    {
        "email": "alice@example.com",
        "name": "Артем",
        "surname": "Степанов",
        "about": "Backend разработчик",
        "phone": "+79990000001",
        "github_url": "https://github.com/alice",
    },
    {
        "email": "bob@example.com",
        "name": "Геннадий",
        "surname": "Горин",
        "about": "Frontend разработчик",
        "phone": "+79990000002",
        "github_url": "https://github.com/bob",
    },
    {
        "email": "carol@example.com",
        "name": "Марк",
        "surname": "Костя",
        "about": "UI/UX дизайнер",
        "phone": "+79990000003",
        "github_url": "https://github.com/carol",
    },
]

DEMO_PROJECTS = [
    {
        "owner_email": "alice@example.com",
        "name": "Task Tracker",
        "description": "Сервис управления задачами для небольшой команды.",
        "status": "open",
        "github_url": "https://github.com/alice/task-tracker",
        "skills": ["Python", "Django", "PostgreSQL"],
    },
    {
        "owner_email": "bob@example.com",
        "name": "UI Kit Showcase",
        "description": "Каталог UI-компонентов с документацией.",
        "status": "open",
        "github_url": "https://github.com/bob/ui-kit-showcase",
        "skills": ["React", "Docker"],
    },
    {
        "owner_email": "carol@example.com",
        "name": "Landing Generator",
        "description": "Конструктор лендингов для pet-проектов.",
        "status": "closed",
        "github_url": "https://github.com/carol/landing-generator",
        "skills": ["Django", "React"],
    },
]


def _get_or_create_skill(Skill, name):
    existing = Skill.objects.filter(name__iexact=name).first()
    if existing is not None:
        return existing
    return Skill.objects.create(name=name)


def create_demo_data(apps, schema_editor):
    User = apps.get_model("users", "User")
    Project = apps.get_model("projects", "Project")
    Skill = apps.get_model("projects", "Skill")

    users_by_email = {}

    for data in DEMO_USERS:
        email = data["email"].lower()
        user = User.objects.filter(email__iexact=email).first()

        if user is None:
            user = User(
                email=email,
                name=data["name"],
                surname=data["surname"],
                about=data["about"],
                phone=data["phone"],
                github_url=data["github_url"],
                is_active=True,
            )
            user.password = make_password(DEMO_PASSWORD)
            user.save()
        else:
            updated = False
            for field in ("name", "surname", "about", "phone", "github_url"):
                if getattr(user, field) != data[field]:
                    setattr(user, field, data[field])
                    updated = True
            if updated:
                user.save()

        users_by_email[email] = user

    for data in DEMO_PROJECTS:
        owner = users_by_email[data["owner_email"]]
        project, _ = Project.objects.get_or_create(
            owner=owner,
            name=data["name"],
            defaults={
                "description": data["description"],
                "status": data["status"],
                "github_url": data["github_url"],
            },
        )

        skill_objects = [_get_or_create_skill(Skill, skill_name) for skill_name in data["skills"]]
        project.skills.set(skill_objects)

    task_tracker = Project.objects.filter(
        owner=users_by_email["alice@example.com"],
        name="Task Tracker",
    ).first()
    ui_kit_showcase = Project.objects.filter(
        owner=users_by_email["bob@example.com"],
        name="UI Kit Showcase",
    ).first()

    if task_tracker is not None:
        task_tracker.participants.add(
            users_by_email["bob@example.com"],
            users_by_email["carol@example.com"],
        )
        task_tracker.favorites.add(users_by_email["bob@example.com"])

    if ui_kit_showcase is not None:
        ui_kit_showcase.participants.add(users_by_email["alice@example.com"])
        ui_kit_showcase.favorites.add(users_by_email["carol@example.com"])


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_add_name_field"),
        ("projects", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(create_demo_data, migrations.RunPython.noop),
    ]
