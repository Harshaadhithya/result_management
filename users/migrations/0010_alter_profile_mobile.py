# Generated by Django 3.2.9 on 2022-01-02 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_profile_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mobile',
            field=models.IntegerField(null=True),
        ),
    ]
