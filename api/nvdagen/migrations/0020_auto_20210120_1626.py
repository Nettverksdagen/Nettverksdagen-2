# Generated by Django 2.2.12 on 2021-01-20 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nvdagen', '0019_auto_20210120_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='timeEnd',
            field=models.IntegerField(null=True),
        ),
    ]