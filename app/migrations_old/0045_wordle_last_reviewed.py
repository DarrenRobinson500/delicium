# Generated by Django 4.2.8 on 2024-01-19 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_tennisgame_game_score_a_tennisgame_game_score_b_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordle',
            name='last_reviewed',
            field=models.DateField(default=None, null=True),
        ),
    ]
