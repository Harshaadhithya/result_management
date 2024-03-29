# Generated by Django 3.2.9 on 2022-01-07 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0027_remove_finalresult_dept'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='finalresult',
            options={'ordering': ['student__roll_no']},
        ),
        migrations.AlterModelOptions(
            name='sempapers',
            options={'ordering': ['-semester__year', 'semester__season', 'dept']},
        ),
        migrations.AlterField(
            model_name='result',
            name='status',
            field=models.BooleanField(choices=[(True, 'Pass'), (False, 'Fail')], default=0),
        ),
    ]
