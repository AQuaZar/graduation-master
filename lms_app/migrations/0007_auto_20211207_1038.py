# Generated by Django 3.2.8 on 2021-12-07 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_app', '0006_rename_grade_task_max_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='file',
            field=models.FileField(blank=True, upload_to='task_docs/'),
        ),
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.CharField(choices=[('QUIZ', 'quiz'), ('BASE', 'basic'), ('MOD', 'module')], max_length=10),
        ),
    ]
