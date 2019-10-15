# Generated by Django 2.2.4 on 2019-10-10 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20191010_0217'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.IntegerField(choices=[(0, 'Keeper'), (1, 'Defence'), (2, 'Midfield'), (3, 'Attack')], default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(0, 'banned'), (1, 'member'), (2, 'moderator'), (3, 'admin')], default=1),
        ),
    ]
