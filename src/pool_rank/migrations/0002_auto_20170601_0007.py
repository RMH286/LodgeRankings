# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-01 00:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pool_rank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poolgame',
            name='loser2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loser2', to='house.Player'),
        ),
        migrations.AlterField(
            model_name='poolgame',
            name='winner2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner2', to='house.Player'),
        ),
    ]
