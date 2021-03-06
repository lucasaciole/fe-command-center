# Generated by Django 3.0.7 on 2020-06-29 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fireshop', '0013_eventattendanceconfirmation'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerpointshistory',
            name='total_points_on_date',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventattendanceconfirmation',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_confirmations', to='fireshop.Event'),
        ),
    ]
