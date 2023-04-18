# Generated by Django 4.2 on 2023-04-17 14:18

from django.db import migrations, models
import stat_track.models


class Migration(migrations.Migration):

    dependencies = [
        ('stat_track', '0007_alter_stats_draws_alter_stats_goals_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stats',
            name='draws',
            field=models.IntegerField(default=0, validators=[stat_track.models.Stats.positive_validator]),
        ),
        migrations.AlterField(
            model_name='stats',
            name='goals',
            field=models.IntegerField(default=0, validators=[stat_track.models.Stats.positive_validator]),
        ),
        migrations.AlterField(
            model_name='stats',
            name='loses',
            field=models.IntegerField(default=0, validators=[stat_track.models.Stats.positive_validator]),
        ),
        migrations.AlterField(
            model_name='stats',
            name='wins',
            field=models.IntegerField(default=0, validators=[stat_track.models.Stats.positive_validator]),
        ),
    ]
