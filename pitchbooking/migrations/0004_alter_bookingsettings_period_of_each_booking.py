# Generated by Django 4.1.4 on 2022-12-22 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pitchbooking', '0003_remove_booking_user_email_remove_booking_user_mobile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingsettings',
            name='period_of_each_booking',
            field=models.CharField(choices=[('60', '1H'), ('90', '1H 30M'), ('120', '2H'), ('150', '2H 30M'), ('180', '3H')], default='60', help_text='How long each booking take.', max_length=3),
        ),
    ]