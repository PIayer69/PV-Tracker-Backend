# Generated by Django 4.1 on 2022-09-11 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_post_produced_all_alter_post_received_all_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='produced',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='produced_all',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='received',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='received_all',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='sent',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='sent_all',
            field=models.FloatField(blank=True),
        ),
    ]