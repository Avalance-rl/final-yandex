from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from projects.models import Project, Skill


class Command(BaseCommand):
    help = "Создает тестовых пользователей и проекты для ревью"

    def handle(self, *args, **options):
        User = get_user_model()

        users_data = [
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

        users = []
        for data in users_data:
            user, created = User.objects.get_or_create(
                email=data["email"],
                defaults={
                    "name": data["name"],
                    "surname": data["surname"],
                    "about": data["about"],
                    "phone": data["phone"],
                    "github_url": data["github_url"],
                },
            )
            if created:
                user.set_password("demo12345")
                user.save(update_fields=["password"])
            else:
                updated_fields = []
                for field in ("name", "surname", "about", "phone", "github_url"):
                    if getattr(user, field) != data[field]:
                        setattr(user, field, data[field])
                        updated_fields.append(field)
                if updated_fields:
                    user.save(update_fields=updated_fields)
            users.append(user)

        skill_names = ["Python", "Django", "PostgreSQL", "React", "Docker"]
        skills = {}
        for name in skill_names:
            skill, _ = Skill.objects.get_or_create(name=name)
            skills[name] = skill

        projects_data = [
            {
                "owner": users[0],
                "name": "Task Tracker",
                "description": "Сервис управления задачами для небольшой команды.",
                "status": Project.STATUS_OPEN,
                "github_url": "https://github.com/alice/task-tracker",
                "skills": ["Python", "Django", "PostgreSQL"],
            },
            {
                "owner": users[1],
                "name": "UI Kit Showcase",
                "description": "Каталог UI-компонентов с документацией.",
                "status": Project.STATUS_OPEN,
                "github_url": "https://github.com/bob/ui-kit-showcase",
                "skills": ["React", "Docker"],
            },
            {
                "owner": users[2],
                "name": "Landing Generator",
                "description": "Конструктор лендингов для pet-проектов.",
                "status": Project.STATUS_CLOSED,
                "github_url": "https://github.com/carol/landing-generator",
                "skills": ["Django", "React"],
            },
        ]

        for data in projects_data:
            project, _ = Project.objects.get_or_create(
                owner=data["owner"],
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "status": data["status"],
                    "github_url": data["github_url"],
                },
            )
            project.skills.set([skills[item] for item in data["skills"]])

        # Небольшие связи между пользователями и проектами.
        projects = list(Project.objects.all())
        if len(projects) >= 2:
            projects[0].participants.add(users[1], users[2])
            projects[1].participants.add(users[0])
            projects[0].favorites.add(users[1])
            projects[1].favorites.add(users[2])

        self.stdout.write(self.style.SUCCESS("Демо-данные созданы. Пароль для всех пользователей: demo12345"))
