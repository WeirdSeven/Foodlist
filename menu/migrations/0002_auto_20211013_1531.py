# Generated by Django 3.2.7 on 2021-10-13 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sdish',
            options={'verbose_name': '菜品', 'verbose_name_plural': '菜品'},
        ),
        migrations.AlterModelOptions(
            name='sdish2standard',
            options={'verbose_name': '菜品标准', 'verbose_name_plural': '菜品标准'},
        ),
        migrations.RenameField(
            model_name='ckproject',
            old_name='sdishe2standards',
            new_name='sdish2standards',
        ),
        migrations.AlterField(
            model_name='ckproject2sdish2standardcount',
            name='project2dish2standard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations_counts', to='menu.ckproject2sdish2standard'),
        ),
        migrations.AlterField(
            model_name='sdish2standardingredient',
            name='sdish2standard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='menu.sdish2standard'),
        ),
    ]