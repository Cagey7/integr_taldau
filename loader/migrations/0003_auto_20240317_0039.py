# Generated by Django 5.0.2 on 2024-03-16 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loader', '0002_dic_indexperiod_alter_chapter_parent_and_more'),
    ]

    operations = [
        migrations.RunSQL('CREATE SCHEMA index_data;'),
        migrations.RunSQL('CREATE SCHEMA dics_data;')
    ]
