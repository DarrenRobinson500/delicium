# Generated by Django 4.2.8 on 2024-01-20 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_wordle_last_reviewed'),
    ]

    operations = [
        migrations.CreateModel(
            name='TennisMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_A', models.IntegerField(blank=True, default=0, null=True)),
                ('score_B', models.IntegerField(blank=True, default=0, null=True)),
                ('game_date', models.DateField(null=True)),
                ('name', models.CharField(max_length=30, null=True)),
                ('player_A', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_A', to='app.tennisplayer')),
                ('player_B', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_B', to='app.tennisplayer')),
            ],
        ),
        migrations.CreateModel(
            name='TennisSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_no', models.IntegerField(blank=True, null=True)),
                ('match', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.tennismatch')),
            ],
        ),
        migrations.RemoveField(
            model_name='tennissetscore',
            name='game',
        ),
        migrations.RemoveField(
            model_name='tennisgame',
            name='game_date',
        ),
        migrations.RemoveField(
            model_name='tennisgame',
            name='game_score_A',
        ),
        migrations.RemoveField(
            model_name='tennisgame',
            name='game_score_B',
        ),
        migrations.RemoveField(
            model_name='tennisgame',
            name='name',
        ),
        migrations.RemoveField(
            model_name='tennisgame',
            name='player_A',
        ),
        migrations.RemoveField(
            model_name='tennisgame',
            name='player_B',
        ),
        migrations.AlterField(
            model_name='tennisgame',
            name='score_A',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tennisgame',
            name='score_B',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='TennisGameScore',
        ),
        migrations.DeleteModel(
            name='TennisSetScore',
        ),
        migrations.AddField(
            model_name='tennisgame',
            name='set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.tennisset'),
        ),
    ]
