# Generated by Django 4.2 on 2023-04-22 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stat_track', '0018_alter_match_away_goals_alter_match_home_goals_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stats',
            options={},
        ),
        migrations.RemoveField(
            model_name='stats',
            name='draws',
        ),
        migrations.RemoveField(
            model_name='stats',
            name='loses',
        ),
        migrations.RemoveField(
            model_name='stats',
            name='wins',
        ),
    ]
