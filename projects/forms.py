from django import forms

from team_finder.constants import PROJECT_DESCRIPTION_ROWS, SKILL_NAME_MAX_LENGTH

from .models import Project, Skill


class ProjectForm(forms.ModelForm):
    skill_names = forms.CharField(
        label="Необходимые навыки",
        required=False,
        help_text="Перечислите навыки через запятую, например: Python, PostgreSQL, Docker.",
    )

    class Meta:
        model = Project
        fields = ("name", "description", "github_url", "status")
        labels = {
            "name": "Название проекта",
            "description": "Описание",
            "github_url": "Ссылка на GitHub",
            "status": "Статус",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": PROJECT_DESCRIPTION_ROWS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["skill_names"].initial = ", ".join(
                self.instance.skills.order_by("name").values_list("name", flat=True)
            )

    def clean_skill_names(self):
        raw_value = self.cleaned_data.get("skill_names", "")
        if not raw_value:
            return []

        normalized_names = []
        seen = set()

        for part in raw_value.split(","):
            name = part.strip()
            if not name:
                continue
            key = name.lower()
            if key in seen:
                continue
            if len(name) > SKILL_NAME_MAX_LENGTH:
                raise forms.ValidationError(
                    f"Название навыка не должно быть длиннее {SKILL_NAME_MAX_LENGTH} символов."
                )
            seen.add(key)
            normalized_names.append(name)

        return normalized_names

    def save_skills(self, project):
        skill_names = self.cleaned_data.get("skill_names", [])
        skills = []
        for name in skill_names:
            existing = Skill.objects.filter(name__iexact=name).first()
            if existing:
                skills.append(existing)
                continue
            skills.append(Skill.objects.create(name=name))

        project.skills.set(skills)
