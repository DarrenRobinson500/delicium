# Generated by Django 4.2.8 on 2024-01-08 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_new_tide'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(null=True)),
                ('precis', models.CharField(max_length=30, null=True)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tide_date')),
            ],
        ),
    ]