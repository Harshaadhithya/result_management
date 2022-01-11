# Generated by Django 3.2.9 on 2021-12-13 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_department_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('admin', 'admin_user'), ('student', 'student_user')], default='admin', max_length=100),
            preserve_default=False,
        ),
    ]
