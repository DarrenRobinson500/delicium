# Generated by Django 4.2.8 on 2024-01-11 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_note_note_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wordle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=5, null=True)),
                ('date', models.DateField(null=True)),
            ],
        ),
    ]
