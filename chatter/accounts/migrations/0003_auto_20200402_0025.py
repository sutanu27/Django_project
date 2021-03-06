# Generated by Django 2.2.10 on 2020-04-01 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='accounts/images/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.TextField(blank=True),
        ),
    ]
