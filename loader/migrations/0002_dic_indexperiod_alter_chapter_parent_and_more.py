# Generated by Django 5.0.2 on 2024-03-15 17:45

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loader', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dic_ids', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('dic_names', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=511), size=None)),
                ('term_ids', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
            ],
            options={
                'db_table': 'dics',
            },
        ),
        migrations.CreateModel(
            name='IndexPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Период индекса')),
            ],
            options={
                'db_table': 'index_periods',
            },
        ),
        migrations.AlterField(
            model_name='chapter',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='loader.chapter'),
        ),
        migrations.AlterField(
            model_name='index',
            name='chapter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='loader.chapter', verbose_name='Раздел'),
        ),
        migrations.AlterModelTable(
            name='chapter',
            table='chapters',
        ),
        migrations.AlterModelTable(
            name='index',
            table='indices',
        ),
        migrations.CreateModel(
            name='IndexDics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dates', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('dics', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='loader.dic')),
                ('index', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='loader.index')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='loader.indexperiod')),
            ],
            options={
                'db_table': 'indices_dics',
            },
        ),
        migrations.CreateModel(
            name='DatePeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Дата индекса')),
                ('index_period', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='loader.indexperiod')),
            ],
            options={
                'db_table': 'date_periods',
            },
        ),
    ]
