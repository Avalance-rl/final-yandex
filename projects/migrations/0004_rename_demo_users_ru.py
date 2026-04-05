from django.db import migrations


def rename_demo_users(apps, schema_editor):
    User = apps.get_model("users", "User")

    mapping = [
        ("alice@example.com", "Артем", "Степанов", "Backend разработчик"),
        ("bob@example.com", "Геннадий", "Горин", "Frontend разработчик"),
        ("carol@example.com", "Марк", "Костя", "UI/UX дизайнер"),
    ]

    for email, name, surname, about in mapping:
        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            continue

        updated = False
        if user.name != name:
            user.name = name
            updated = True
        if user.surname != surname:
            user.surname = surname
            updated = True
        if user.about != about:
            user.about = about
            updated = True

        if updated:
            user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0003_seed_demo_data"),
    ]

    operations = [
        migrations.RunPython(rename_demo_users, migrations.RunPython.noop),
    ]

