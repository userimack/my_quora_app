# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-25 19:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0014_auto_20180226_0114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rateanswer',
            old_name='Answer',
            new_name='answer',
        ),
    ]
