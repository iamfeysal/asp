# Generated by Django 2.2.4 on 2020-03-24 00:42

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.SlugField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=255, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=100, verbose_name='last name')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('avatar', models.ImageField(default='avatars/default/user.png', upload_to='avatars/%Y/%m')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_player', models.BooleanField(default=True, verbose_name='player status')),
                ('is_coach', models.BooleanField(default=False, verbose_name='coach status')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('role', models.IntegerField(choices=[(0, 'banned'), (1, 'member'), (2, 'moderator'), (3, 'admin')], default=1)),
                ('position', models.IntegerField(choices=[(0, 'Keeper'), (1, 'Defence'), (2, 'Midfield'), (3, 'Attack')], default=1)),
                ('followers', models.ManyToManyField(blank=True, related_name='followers_set', to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(blank=True, related_name='following_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'permissions': (('view_category', 'view category'), ('add_category', 'Add category'), ('delete_category', 'Delete category')),
            },
        ),
        migrations.CreateModel(
            name='UserFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True)),
                ('date_submitted', models.DateTimeField(null=True)),
                ('message_polarity', models.CharField(blank=True, choices=[('positive', 'Positive Experience'), ('negative', 'Negative Experience'), ('undefined', 'Undefined')], default='undefined', max_length=50, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('like', 'Like'), ('comment', 'Comment'), ('follow', 'Follow')], max_length=20)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='creator', to=settings.AUTH_USER_MODEL)),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-notification_type'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='skills',
            field=models.ManyToManyField(to='users.Skill'),
        ),
    ]
