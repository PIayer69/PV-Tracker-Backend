# Generated by Django 4.1 on 2022-09-09 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='autoconsumption_percentage',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='consumption_average',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
