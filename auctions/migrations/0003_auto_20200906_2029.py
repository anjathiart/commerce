# Generated by Django 3.1 on 2020-09-06 20:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200906_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='listing', to='auctions.Comment'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='watchListings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listingsWon', to=settings.AUTH_USER_MODEL),
        ),
    ]
