# Generated by Django 4.2.8 on 2024-01-19 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_tennisgame_tennisgamescore_game_tennissetscore_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='tennisgame',
            name='score_A',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tennisgame',
            name='score_B',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
