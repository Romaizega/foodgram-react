# Generated by Django 4.2.9 on 2024-02-10 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_remove_fooduser_is_subscribed'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooduser',
            name='is_subscribed',
            field=models.BooleanField(default=False),
        ),
    ]
