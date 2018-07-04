# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-09 15:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='ingredients',
            field=models.ManyToManyField(through='menu.Food2Ingredient', to='menu.Ingredient'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]