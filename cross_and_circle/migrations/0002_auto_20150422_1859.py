# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cross_and_circle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('position', models.PositiveSmallIntegerField()),
                ('game', models.ForeignKey(to='cross_and_circle.Player')),
                ('player', models.ForeignKey(related_name='all_moves', to='cross_and_circle.Player')),
            ],
        ),
        migrations.RemoveField(
            model_name='game',
            name='board',
        ),
        migrations.AlterField(
            model_name='gamerequest',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='GameBoard',
        ),
    ]
