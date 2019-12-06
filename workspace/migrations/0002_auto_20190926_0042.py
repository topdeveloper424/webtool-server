# Generated by Django 2.2.3 on 2019-09-26 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='status',
            field=models.CharField(choices=[('R', 'ready for review'), ('P', 'pending'), ('A', 'approved'), ('S', 'sent to import'), ('D', 'deleted')], default='R', max_length=4),
        ),
        migrations.AlterField(
            model_name='record',
            name='free',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='record',
            name='tickets_at_door_only',
            field=models.BooleanField(default=False),
        ),
    ]
