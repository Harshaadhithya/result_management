# Generated by Django 3.2.9 on 2022-01-03 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_profile_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='dept_expansion',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]