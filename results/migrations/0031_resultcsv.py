# Generated by Django 3.2.9 on 2022-01-30 08:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0030_auto_20220110_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultCsv',
            fields=[
                ('file_name', models.FileField(upload_to='csvfiles/')),
                ('activated', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]