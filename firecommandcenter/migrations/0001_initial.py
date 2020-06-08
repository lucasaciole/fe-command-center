# Generated by Django 3.0.7 on 2020-06-08 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassTree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('class_tree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firecommandcenter.ClassTree')),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('class_tree', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='firecommandcenter.ClassTree')),
                ('first_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='firecommandcenter.Class')),
                ('second_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='firecommandcenter.Class')),
                ('thrid_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='firecommandcenter.Class')),
            ],
        ),
    ]
