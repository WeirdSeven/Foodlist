# Generated by Django 3.2.10 on 2022-01-25 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchasing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpurchaseorder',
            name='status',
            field=models.CharField(choices=[('EDT', '编辑中'), ('SBM', '已提交'), ('APR', '️️通过'), ('REJ', '未通过'), ('RED', '重新编辑中'), ('RSB', '已重新提交')], default='EDT', max_length=3, verbose_name='状态'),
        ),
    ]