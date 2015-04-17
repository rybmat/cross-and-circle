# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('started', models.DateTimeField(auto_now_add=True)),
                ('finished', models.DateTimeField(default=None, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GameBoard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('f_00', models.CharField(max_length=1, null=True, blank=True)),
                ('f_01', models.CharField(max_length=1, null=True, blank=True)),
                ('f_02', models.CharField(max_length=1, null=True, blank=True)),
                ('f_10', models.CharField(max_length=1, null=True, blank=True)),
                ('f_11', models.CharField(max_length=1, null=True, blank=True)),
                ('f_12', models.CharField(max_length=1, null=True, blank=True)),
                ('f_20', models.CharField(max_length=1, null=True, blank=True)),
                ('f_21', models.CharField(max_length=1, null=True, blank=True)),
                ('f_22', models.CharField(max_length=1, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GameRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('won', models.PositiveIntegerField(default=0)),
                ('lost', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='gamerequest',
            name='requested',
            field=models.ForeignKey(related_name='requested', to='cross_and_circle.Player'),
        ),
        migrations.AddField(
            model_name='gamerequest',
            name='requesting',
            field=models.ForeignKey(related_name='requesting', to='cross_and_circle.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='board',
            field=models.OneToOneField(to='cross_and_circle.GameBoard'),
        ),
        migrations.AddField(
            model_name='game',
            name='player_a',
            field=models.ForeignKey(related_name='player_a', to='cross_and_circle.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='player_b',
            field=models.ForeignKey(related_name='player_b', to='cross_and_circle.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(default=None, blank=True, to='cross_and_circle.Player', null=True),
        ),
    ]
