# Generated by Django 2.2.28 on 2023-10-18 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nvdagen', '0027_auto_20231018_1246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='business',
            old_name='standpos_x',
            new_name='standpos',
        ),
        migrations.RemoveField(
            model_name='business',
            name='standpos_y',
        ),
    ]
