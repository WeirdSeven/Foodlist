# Generated by Django 3.2.7 on 2021-12-22 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='specification',
            field=models.CharField(blank=True, max_length=200, verbose_name='规格'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(choices=[('JN', '斤'), ('KG', '公斤'), ('BT', '瓶'), ('BK', '桶'), ('BX', '箱'), ('SK', '袋'), ('BG', '包')], default='JN', max_length=2, verbose_name='单位'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='category',
            field=models.CharField(choices=[('VG', '蔬果'), ('MT', '肉类'), ('TF', '豆制品'), ('CND', '调料'), ('DRY', '干货'), ('RNO', '米面油'), ('DSP', '低值易耗')], default='VG', max_length=3, verbose_name='原材料分类'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='price',
            field=models.FloatField(verbose_name='单价'),
        ),
    ]
