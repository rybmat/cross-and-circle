# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cross_and_circle', '0002_auto_20150422_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='user',
        ),
        migrations.AlterField(
            model_name='game',
            name='player_a',
            field=models.ForeignKey(related_name='player_a', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='game',
            name='player_b',
            field=models.ForeignKey(related_name='player_b', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='gamerequest',
            name='requested',
            field=models.ForeignKey(related_name='requested', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='gamerequest',
            name='requesting',
            field=models.ForeignKey(related_name='requesting', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='move',
            name='game',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='move',
            name='player',
            field=models.ForeignKey(related_name='all_moves', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Player',
        ),
    ]
