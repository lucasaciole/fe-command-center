# Generated by Django 3.0.7 on 2020-06-15 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fireshop', '0005_auto_20200615_1518'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='event_name',
            new_name='name',
        ),
    ]
