from django.db import migrations, models


def fill_name_from_first_name(apps, schema_editor):
    User = apps.get_model("users", "User")
    for user in User.objects.filter(name=""):
        user.name = user.first_name
        user.save(update_fields=["name"])


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="name",
            field=models.CharField(default="", max_length=150, verbose_name="Имя"),
            preserve_default=False,
        ),
        migrations.RunPython(fill_name_from_first_name, migrations.RunPython.noop),
    ]
