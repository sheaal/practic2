# Generated by Django 4.2.7 on 2023-11-24 16:18

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.utilities


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_activated', models.BooleanField(db_index=True, default=True, verbose_name='Прошел активацию?')),
                ('send_messages', models.BooleanField(default=True, verbose_name='Оповещать при новых комментариях?')),
                ('sur_name', models.CharField(max_length=200, verbose_name='Фамилия')),
                ('n_name', models.CharField(max_length=200, verbose_name='Имя')),
                ('pat_mic', models.CharField(max_length=200, verbose_name='Отчество')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_title', models.CharField(max_length=200, verbose_name='Название категории')),
            ],
        ),
        migrations.CreateModel(
            name='Applic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='Название заявки')),
                ('content', models.TextField(verbose_name='Описание заявки')),
                ('image', models.ImageField(blank=True, upload_to='design1', verbose_name='Изображение')),
                ('data', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')),
                ('status', models.CharField(choices=[('Новая', 'Новая'), ('Принято в работу', 'Принято в работу'), ('Выполнено', 'Выполнено')], default='Новая', max_length=70, verbose_name='Статус')),
                ('comment', models.TextField(blank=True)),
                ('image_design', models.ImageField(blank=True, upload_to='design/', verbose_name='Фотография')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-data'],
            },
        ),
        migrations.CreateModel(
            name='AdditionalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=main.utilities.get_timestamp_path, verbose_name='Фотография')),
                ('bb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.applic', verbose_name='Заявка')),
            ],
        ),
    ]
