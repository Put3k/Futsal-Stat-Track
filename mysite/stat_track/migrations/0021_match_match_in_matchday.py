# Generated by Django 4.2 on 2023-04-23 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stat_track', '0020_matchday_match_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='match_in_matchday',
            field=models.IntegerField(default=0),
        ),
    ]
