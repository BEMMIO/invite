# Generated by Django 3.2.7 on 2021-09-07 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210907_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='invite_code',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='Invite Code'),
        ),
    ]
