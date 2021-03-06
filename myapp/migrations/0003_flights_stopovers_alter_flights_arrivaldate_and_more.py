# Generated by Django 4.0.4 on 2022-05-31 04:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_flights_arrivaldate_alter_flights_leavingdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='flights',
            name='stopOvers',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='flights',
            name='arrivalDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 31, 4, 12, 58, 386979, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='flights',
            name='leavingDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 31, 4, 12, 58, 386979, tzinfo=utc)),
        ),
    ]
