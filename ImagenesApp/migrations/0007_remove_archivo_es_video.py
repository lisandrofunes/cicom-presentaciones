# Generated by Django 4.2.4 on 2023-08-31 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ImagenesApp', '0006_remove_archivo_tipo_archivo_es_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archivo',
            name='es_video',
        ),
    ]
