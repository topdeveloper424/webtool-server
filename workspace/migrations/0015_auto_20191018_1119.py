# Generated by Django 2.2.5 on 2019-10-18 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0014_auto_20191015_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='detail',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='ticket_url',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]
