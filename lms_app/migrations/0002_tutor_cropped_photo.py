# Generated by Django 3.2.8 on 2021-11-29 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='cropped_photo',
            field=models.ImageField(blank=True, upload_to='tutors'),
        ),
    ]