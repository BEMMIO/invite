# Generated by Django 3.2.7 on 2021-09-07 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invite', '0002_alter_invitation_invite_to_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invitation',
            options={'verbose_name': 'User invitation', 'verbose_name_plural': 'User invitation'},
        ),
    ]
