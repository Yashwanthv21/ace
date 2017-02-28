# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 04:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usersimei',
            unique_together=set([('imei_numbers', 'user')]),
        ),
    ]