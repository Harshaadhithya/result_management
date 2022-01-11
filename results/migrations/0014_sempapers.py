# Generated by Django 3.2.9 on 2021-12-07 16:41

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_department_name'),
        ('results', '0013_delete_sempapers'),
    ]

    operations = [
        migrations.CreateModel(
            name='SemPapers',
            fields=[
                ('year_of_study', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.department')),
                ('semester', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.semester')),
                ('subjects', models.ManyToManyField(blank=True, to='results.Subject')),
            ],
        ),
    ]
