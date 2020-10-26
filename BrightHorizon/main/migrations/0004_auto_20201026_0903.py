# Generated by Django 3.1.2 on 2020-10-26 13:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_task_points_worth'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usertask',
            old_name='task_completed',
            new_name='task',
        ),
        migrations.RemoveField(
            model_name='task',
            name='is_completed',
        ),
        migrations.RemoveField(
            model_name='usergoal',
            name='suggested_complete_date',
        ),
        migrations.RemoveField(
            model_name='usertask',
            name='goal',
        ),
        migrations.RemoveField(
            model_name='usertask',
            name='points',
        ),
        migrations.AddField(
            model_name='goal',
            name='points_worth',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='usergoal',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='usertask',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
