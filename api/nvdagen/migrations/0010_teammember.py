# Generated by Django 2.1.5 on 2019-01-11 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nvdagen', '0009_listing_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=250)),
                ('photo_uri', models.CharField(max_length=250)),
                ('team', models.CharField(max_length=250)),
                ('position', models.CharField(max_length=250)),
            ],
        ),
    ]
