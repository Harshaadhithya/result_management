# Generated by Django 3.2.9 on 2022-01-03 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_department_dept_expansion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='profile',
            new_name='profile_img',
        ),
    ]