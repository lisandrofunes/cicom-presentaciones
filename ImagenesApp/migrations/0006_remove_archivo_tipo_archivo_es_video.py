# Generated by Django 4.2.4 on 2023-08-31 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ImagenesApp', '0005_archivo_tipo_alter_archivo_archivo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archivo',
            name='tipo',
        ),
        migrations.AddField(
            model_name='archivo',
            name='es_video',
            field=models.BooleanField(default=False),
        ),
    ]
