# Generated by Django 3.2.7 on 2021-09-07 12:07

import apps.invite.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=apps.invite.models.get_default_uuid, editable=False, max_length=32, unique=True)),
                ('invite_to_email', models.EmailField(max_length=255)),
                ('invite_token', models.CharField(blank=True, max_length=15, null=True, verbose_name='token')),
                ('invite_message', models.TextField(blank=True, max_length=225, null=True, verbose_name='message')),
                ('invite_choices', models.CharField(blank=True, choices=[('accepted', 'Accepted'), ('rejected', 'Rejected'), ('sent', 'Sent')], max_length=10, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('invite_from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invites_from_user', to=settings.AUTH_USER_MODEL, verbose_name='invitation from user')),
            ],
            options={
                'unique_together': {('invite_from_user', 'invite_to_email', 'invite_token')},
            },
        ),
    ]
