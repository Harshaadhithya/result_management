# Generated by Django 3.2.9 on 2022-01-03 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_department_dept_expansion'),
        ('results', '0018_subject_subject_expansion'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sempapers',
            unique_together={('dept', 'semester', 'year_of_study')},
        ),
    ]