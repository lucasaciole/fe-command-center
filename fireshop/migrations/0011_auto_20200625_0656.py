# Generated by Django 3.0.7 on 2020-06-25 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fireshop', '0010_auto_20200615_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventattendance',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='fireshop.Event'),
        ),
        migrations.AlterField(
            model_name='eventattendance',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_attendances', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='eventattendancecategory',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_categories', to='fireshop.Event'),
        ),
    ]
