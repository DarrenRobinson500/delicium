# Generated by Django 4.2.8 on 2024-01-12 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_dog_owners_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='owners_link',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.note'),
        ),
    ]
