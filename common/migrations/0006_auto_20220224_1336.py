# Generated by Django 3.2.10 on 2022-02-24 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_alter_ingredientprice_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='category',
            field=models.CharField(choices=[('VG', '蔬果'), ('MT', '肉类'), ('SD', '副食'), ('TF', '豆制品'), ('CND', '调料'), ('DRY', '干货'), ('RNO', '米面油'), ('DSP', '低值易耗')], default='VG', max_length=3, verbose_name='分类'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(choices=[('JN', '斤'), ('KG', '公斤'), ('BT', '瓶'), ('BK', '桶'), ('BX', '箱'), ('SK', '袋'), ('BG', '包'), ('SN', '个'), ('PR', '副')], default='JN', max_length=2, verbose_name='单位'),
        ),
    ]
