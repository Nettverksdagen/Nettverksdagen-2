# Generated by Django 2.2.12 on 2021-01-22 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nvdagen', '0022_merge_20210120_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='study',
            field=models.CharField(default='string', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='year',
            field=models.CharField(default='String', max_length=250),
            preserve_default=False,
        ),
    ]
