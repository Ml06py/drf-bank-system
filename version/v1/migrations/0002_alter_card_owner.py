# Generated by Django 4.0.4 on 2022-07-22 06:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('v1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='owner',
            field=models.ManyToManyField(related_name='cards', to=settings.AUTH_USER_MODEL),
        ),
    ]
