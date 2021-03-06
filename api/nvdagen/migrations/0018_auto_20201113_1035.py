# Generated by Django 2.2.12 on 2020-11-13 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nvdagen', '0017_auto_20200123_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('event', models.IntegerField()),
                ('email', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.AlterField(
            model_name='teammember',
            name='photo_uri',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
    ]
