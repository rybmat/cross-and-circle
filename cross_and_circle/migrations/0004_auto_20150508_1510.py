# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cross_and_circle', '0003_auto_20150422_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='POEToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(unique=True, max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='move',
            name='game',
            field=models.ForeignKey(to='cross_and_circle.Game'),
        ),
        migrations.AlterUniqueTogether(
            name='move',
            unique_together=set([('game', 'position')]),
        ),
    ]
