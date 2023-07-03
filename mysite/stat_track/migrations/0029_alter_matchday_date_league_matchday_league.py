# Generated by Django 4.1.9 on 2023-07-03 17:48

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stat_track', '0028_alter_matchday_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchday',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Date of match'),
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='matchday',
            name='league',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stat_track.league'),
        ),
    ]