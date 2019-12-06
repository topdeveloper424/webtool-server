# Generated by Django 2.2.3 on 2019-09-26 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0002_auto_20190926_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='status',
            field=models.CharField(choices=[('R', 'ready for review'), ('A', 'approved'), ('S', 'sent to import')], default='R', max_length=4),
        ),
    ]
