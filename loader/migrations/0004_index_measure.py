# Generated by Django 5.0.2 on 2024-03-19 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loader', '0003_auto_20240317_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='index',
            name='measure',
            field=models.CharField(max_length=255, null=True, verbose_name='Единица измерения'),
        ),
    ]
