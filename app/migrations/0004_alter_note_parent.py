# Generated by Django 4.2.8 on 2023-12-29 00:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_note_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.note'),
        ),
    ]
