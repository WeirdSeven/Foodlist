# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-11 14:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20160809_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Dish2Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.Dish')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.Ingredient')),
            ],
        ),
        migrations.RemoveField(
            model_name='food',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='food2ingredient',
            name='food',
        ),
        migrations.RemoveField(
            model_name='food2ingredient',
            name='ingredient',
        ),
        migrations.DeleteModel(
            name='Food',
        ),
        migrations.DeleteModel(
            name='Food2Ingredient',
        ),
        migrations.AddField(
            model_name='dish',
            name='ingredients',
            field=models.ManyToManyField(through='menu.Dish2Ingredient', to='menu.Ingredient'),
        ),
    ]
