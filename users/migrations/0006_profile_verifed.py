# Generated by Django 3.2.9 on 2021-12-14 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='verifed',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
