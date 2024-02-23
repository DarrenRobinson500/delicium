# Generated by Django 4.2.8 on 2024-01-08 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_tide_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='New_Tide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(null=True)),
                ('height', models.FloatField()),
                ('type', models.CharField(max_length=10, null=True)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tide_date')),
            ],
        ),
    ]
