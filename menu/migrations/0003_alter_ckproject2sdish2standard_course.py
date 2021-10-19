# Generated by Django 3.2.7 on 2021-10-19 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20211013_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ckproject2sdish2standard',
            name='course',
            field=models.CharField(choices=[('PM', '主荤'), ('SM', '次荤'), ('VG', '素菜'), ('SP', '特色'), ('FR', '水果'), ('GR', '杂粮'), ('SU', '汤粥'), ('ST', '主食'), ('SD', '副食'), ('CD', '凉菜'), ('PK', '咸菜')], default='PM', max_length=2, verbose_name='菜品分类'),
        ),
    ]