# Generated by Django 5.1.6 on 2025-02-15 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='data_joined',
            new_name='date_joined',
        ),
    ]
