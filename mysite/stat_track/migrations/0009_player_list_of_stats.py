# Generated by Django 4.2 on 2023-04-17 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stat_track', '0008_alter_stats_draws_alter_stats_goals_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='list_of_stats',
            field=models.ManyToManyField(related_name='players', to='stat_track.stats'),
        ),
    ]
