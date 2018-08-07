# Generated by Django 2.0.7 on 2018-08-05 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_auto_20180706_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='调料名称')),
                ('price', models.FloatField()),
            ],
            options={
                'verbose_name': '调料',
                'verbose_name_plural': '调料',
            },
        ),
        migrations.CreateModel(
            name='CongeeSoup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='汤粥名称')),
            ],
            options={
                'verbose_name': '汤粥',
                'verbose_name_plural': '汤粥',
            },
        ),
        migrations.CreateModel(
            name='CongeeSoup2Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(verbose_name='重量')),
                ('congeesoup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.CongeeSoup', verbose_name='汤粥名称')),
            ],
            options={
                'verbose_name': '汤粥的配菜',
                'verbose_name_plural': '汤粥的配菜',
            },
        ),
        migrations.CreateModel(
            name='Disposable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='一次性用品名称')),
                ('price', models.FloatField()),
            ],
            options={
                'verbose_name': '一次性用品',
                'verbose_name_plural': '一次性用品',
            },
        ),
        migrations.CreateModel(
            name='Oil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='油名称')),
                ('price', models.FloatField()),
            ],
            options={
                'verbose_name': '油',
                'verbose_name_plural': '油',
            },
        ),
        migrations.CreateModel(
            name='Program2Condiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='份数')),
                ('condiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.Condiment', verbose_name='调料名称')),
            ],
            options={
                'verbose_name': '项目的调料',
                'verbose_name_plural': '项目的调料',
            },
        ),
        migrations.CreateModel(
            name='Program2CongeeSoup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='份数')),
                ('congeesoup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.CongeeSoup', verbose_name='汤粥名称')),
            ],
            options={
                'verbose_name': '项目的汤粥',
                'verbose_name_plural': '项目的汤粥',
            },
        ),
        migrations.CreateModel(
            name='Program2Disposable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='份数')),
                ('disposable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.Disposable', verbose_name='一次性用品名称')),
            ],
            options={
                'verbose_name': '项目的一次性用品',
                'verbose_name_plural': '项目的一次性用品',
            },
        ),
        migrations.CreateModel(
            name='Program2Oil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='份数')),
                ('oil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.Oil', verbose_name='油名称')),
            ],
            options={
                'verbose_name': '项目的油',
                'verbose_name_plural': '项目的油',
            },
        ),
        migrations.CreateModel(
            name='Program2Staple',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='份数')),
            ],
            options={
                'verbose_name': '项目的主食',
                'verbose_name_plural': '项目的主食',
            },
        ),
        migrations.CreateModel(
            name='Staple',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='主食名称')),
                ('price', models.FloatField()),
            ],
            options={
                'verbose_name': '主食',
                'verbose_name_plural': '主食',
            },
        ),
        migrations.CreateModel(
            name='SuperProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='大项目名称')),
            ],
            options={
                'verbose_name': '大项目',
                'verbose_name_plural': '大项目',
            },
        ),
        migrations.AlterModelOptions(
            name='dish2ingredient',
            options={'verbose_name': '菜品的配菜', 'verbose_name_plural': '菜品的配菜'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': '配菜', 'verbose_name_plural': '配菜'},
        ),
        migrations.AddField(
            model_name='program',
            name='condiments',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dish2ingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.Ingredient', verbose_name='配菜名称'),
        ),
        migrations.AddField(
            model_name='program2staple',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.Program', verbose_name='项目名称'),
        ),
        migrations.AddField(
            model_name='program2staple',
            name='staple',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.Staple', verbose_name='主食名称'),
        ),
        migrations.AddField(
            model_name='program2oil',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.Program', verbose_name='项目名称'),
        ),
        migrations.AddField(
            model_name='program2disposable',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.Program', verbose_name='项目名称'),
        ),
        migrations.AddField(
            model_name='program2congeesoup',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.Program', verbose_name='项目名称'),
        ),
        migrations.AddField(
            model_name='program2condiment',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.Program', verbose_name='项目名称'),
        ),
        migrations.AddField(
            model_name='congeesoup2ingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.Ingredient', verbose_name='配菜名称'),
        ),
        migrations.AddField(
            model_name='congeesoup',
            name='ingredient',
            field=models.ManyToManyField(through='menu.CongeeSoup2Ingredient', to='menu.Ingredient'),
        ),
        migrations.AddField(
            model_name='program',
            name='congeesoups',
            field=models.ManyToManyField(through='menu.Program2CongeeSoup', to='menu.CongeeSoup'),
        ),
        migrations.AddField(
            model_name='program',
            name='disposables',
            field=models.ManyToManyField(through='menu.Program2Disposable', to='menu.Disposable'),
        ),
        migrations.AddField(
            model_name='program',
            name='oil',
            field=models.ManyToManyField(through='menu.Program2Oil', to='menu.Oil'),
        ),
        migrations.AddField(
            model_name='program',
            name='staples',
            field=models.ManyToManyField(through='menu.Program2Staple', to='menu.Staple'),
        ),
        migrations.AddField(
            model_name='program',
            name='superprogram',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='menu.SuperProgram', verbose_name='大项目名称'),
        ),
    ]
