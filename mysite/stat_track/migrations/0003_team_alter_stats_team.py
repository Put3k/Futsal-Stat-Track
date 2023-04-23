# Generated by Django 4.2 on 2023-04-17 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stat_track', '0002_alter_match_players_stats'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_color', models.CharField(max_length=16, verbose_name='Team')),
            ],
        ),
        migrations.AlterField(
            model_name='stats',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stat_track.team'),
        ),
    ]