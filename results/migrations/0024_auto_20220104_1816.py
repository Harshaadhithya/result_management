# Generated by Django 3.2.9 on 2022-01-04 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0023_alter_result_grade_string'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='finalresult',
            name='no_of_arrears',
            field=models.IntegerField(default=0),
        ),
    ]
