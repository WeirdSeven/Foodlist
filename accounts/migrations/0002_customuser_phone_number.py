# Generated by Django 3.2.7 on 2021-12-01 04:43

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='11111111111', max_length=128, region=None),
            preserve_default=False,
        ),
    ]
