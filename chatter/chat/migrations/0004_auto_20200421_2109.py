# Generated by Django 2.2.10 on 2020-04-21 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chatroom_group_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_message', to='chat.ChatRoom'),
        ),
    ]