# Generated by Django 4.2.8 on 2024-01-06 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_shop_shopping_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
