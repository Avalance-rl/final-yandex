from django.db import migrations, models
import django.utils.timezone
import users.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='Пароль')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='Последний вход')),
                ('is_superuser', models.BooleanField(default=False, help_text='Дает все права без явного назначения.', verbose_name='Статус суперпользователя')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='Фамилия')),
                ('is_staff', models.BooleanField(default=False, help_text='Разрешает вход в административную панель.', verbose_name='Статус администратора')),
                ('is_active', models.BooleanField(default=True, help_text='Определяет, активна ли учетная запись. Снимите флаг вместо удаления.', verbose_name='Активен')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата регистрации')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('surname', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('about', models.TextField(blank=True, verbose_name='О себе')),
                ('phone', models.CharField(blank=True, max_length=32, verbose_name='Телефон')),
                ('github_url', models.URLField(blank=True, verbose_name='GitHub')),
                ('avatar', models.FileField(blank=True, null=True, upload_to='avatars/', verbose_name='Аватар')),
                ('groups', models.ManyToManyField(blank=True, help_text='Группы пользователя. Права групп применяются к пользователю автоматически.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='Группы')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Индивидуальные права пользователя.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='Права пользователя')),
            ],
            options={
                'ordering': ('-date_joined',),
            },
            managers=[
                ('objects', users.managers.UserManager()),
            ],
        ),
    ]
