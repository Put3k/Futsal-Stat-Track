# Generated by Django 4.2 on 2023-04-17 14:07

from django.db import migrations, models
import stat_track.models


class Migration(migrations.Migration):

    dependencies = [
        ('stat_track', '0004_alter_stats_team_delete_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stats',
            name='draws',
            field=models.IntegerField(validators=[stat_track.models.Stat.positive_validator]),
        ),
        migrations.AlterField(
            model_name='stats',
            name='goals',
            field=models.IntegerField(validators=[stat_track.models.Stat.positive_validator]),
        ),
        migrations.AlterField(
            model_name='stats',
            name='loses',
            field=models.IntegerField(validators=[stat_track.models.Stat.positive_validator]),
        ),
        migrations.AlterField(
            model_name='stats',
            name='wins',
            field=models.IntegerField(validators=[stat_track.models.Stat.positive_validator]),
        ),
    ]
