# Generated by Django 3.2.4 on 2021-11-19 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_examtime_finish_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='question_nums',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='paper',
            name='time_minute',
            field=models.PositiveIntegerField(default=0),
        ),
    ]