# Generated by Django 3.0.7 on 2020-06-11 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fireshop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopitem',
            name='image',
            field=models.ImageField(default=None, upload_to='shop_items/'),
            preserve_default=False,
        ),
    ]
