# Generated by Django 2.2.10 on 2020-04-22 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20200421_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]
