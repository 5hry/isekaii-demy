# Generated by Django 4.2.15 on 2024-08-27 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_avt_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='avt_url',
            field=models.ImageField(default='user_avt/default_avt.png', upload_to='user_avt/'),
        ),
    ]
