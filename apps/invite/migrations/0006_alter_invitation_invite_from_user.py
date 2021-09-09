# Generated by Django 3.2.7 on 2021-09-08 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invite', '0005_auto_20210908_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='invite_from_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invites_from_user', to=settings.AUTH_USER_MODEL, verbose_name='invitation from user'),
        ),
    ]
