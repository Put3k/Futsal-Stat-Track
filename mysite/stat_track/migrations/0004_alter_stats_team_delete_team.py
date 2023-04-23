# Generated by Django 4.2 on 2023-04-17 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stat_track', '0003_team_alter_stats_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stats',
            name='team',
            field=models.CharField(choices=[('Blue', 'Team Blue'), ('Orange', 'Team Orange'), ('Colors', 'Team Colors')], max_length=16),
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]