# Generated by Django 2.2.5 on 2019-10-14 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0012_auto_20191009_2019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='log',
            name='sent_import',
        ),
    ]
