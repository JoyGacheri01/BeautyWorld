# Generated by Django 5.1.3 on 2024-12-08 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
