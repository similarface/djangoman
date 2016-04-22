# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-18 08:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='\u6587\u7ae0\u6807\u9898')),
                ('zhaiyao', models.TextField(verbose_name='\u6458\u8981')),
                ('content', models.TextField(verbose_name='\u6587\u7ae0\u5185\u5bb9')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4f5c\u8005')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u63d0\u4ea4\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('status', models.CharField(choices=[('draft', '\u8349\u7a3f'), ('published', '\u53d1\u5e03')], max_length=10)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
    ]
