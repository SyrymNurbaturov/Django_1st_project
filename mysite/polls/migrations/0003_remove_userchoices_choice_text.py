# Generated by Django 4.1.5 on 2023-02-08 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_userchoices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userchoices',
            name='choice_text',
        ),
    ]
