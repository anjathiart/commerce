# Generated by Django 3.1 on 2020-09-07 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200906_2029'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ['-value']},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='bid',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='listing',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='bidListings', to='auctions.Bid'),
        ),
    ]
