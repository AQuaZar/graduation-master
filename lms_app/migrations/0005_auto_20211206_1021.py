# Generated by Django 3.2.8 on 2021-12-06 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_app', '0004_auto_20211129_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='file',
            field=models.FileField(blank=True, upload_to='task_docs/', verbose_name='Document'),
        ),
        migrations.AlterField(
            model_name='student',
            name='department',
            field=models.CharField(choices=[('feba', 'FEBA'), ('fmv', 'FMV'), ('fabd', 'FABD'), ('faet', 'FAET'), ('uf', 'UF'), ('akf', 'AKF'), ('fccpi', 'FCCPI'), ('ftml', 'FTML'), ('flsk', 'FLSK')], max_length=5),
        ),
        migrations.AlterField(
            model_name='task',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.CharField(choices=[('quiz', 'QUIZ'), ('basic', 'BASE'), ('module', 'MOD')], max_length=10),
        ),
    ]