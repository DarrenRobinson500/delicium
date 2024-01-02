# Generated by Django 4.2.8 on 2024-01-02 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_booking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='dog',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
