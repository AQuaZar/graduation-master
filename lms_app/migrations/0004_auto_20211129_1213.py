# Generated by Django 3.2.8 on 2021-11-29 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms_app', '0003_student_cropped_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='cropped_photo',
        ),
        migrations.RemoveField(
            model_name='tutor',
            name='cropped_photo',
        ),
    ]
