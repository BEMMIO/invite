# Generated by Django 3.2.7 on 2021-09-07 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='invite_to_email',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]