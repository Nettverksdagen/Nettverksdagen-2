# Generated by Django 2.1.3 on 2018-11-27 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nvdagen', '0003_listing_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='logo_uri',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]