# Generated by Django 3.1 on 2020-09-01 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listing_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
