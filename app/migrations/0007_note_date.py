# Generated by Django 4.2.8 on 2023-12-29 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_diary'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
