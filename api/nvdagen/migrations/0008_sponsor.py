# Generated by Django 2.1.3 on 2018-12-17 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nvdagen', '0007_business'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('name', models.CharField(max_length=250)),
                ('logo_uri', models.CharField(max_length=250)),
                ('website_url', models.CharField(max_length=250)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
