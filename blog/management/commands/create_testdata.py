#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0 Beta
@author: Deepak
@license: MIT Licence
@contact: medgloss@gmail.com
@site: https://www.medgloss.com//
@software: Visual Studio Code
@file: create_testdata.py
"""

from django.core.management.base import BaseCommand
from blog.models import Article, Tag, Category
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
import datetime


class Command(BaseCommand):
    help = 'create test datas'

    def handle(self, *args, **options):
        user = get_user_model().objects.get_or_create(
            email='medglosst@gmail.com', username='medgloss', password='r b s k d ')[0]

        pcategory = Category.objects.get_or_create(
            name='I am the parent catagory', parent_category=None)[0]

        category = Category.objects.get_or_create(
            name='Sub-categories', parent_category=pcategory)[0]

        category.save()
        basetag = Tag()
        basetag.name = "label"
        basetag.save()
        for i in range(1, 20):
            article = Article.objects.get_or_create(
                category=category,
                title='nice title ' + str(i),
                body='nice content ' + str(i),
                author=user)[0]
            tag = Tag()
            tag.name = "label" + str(i)
            tag.save()
            article.tags.add(tag)
            article.tags.add(basetag)
            article.save()

        from Medgloss.utils import cache
        cache.clear()
        self.stdout.write(self.style.SUCCESS('created test datas \n'))
