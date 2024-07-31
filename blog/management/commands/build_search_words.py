#!/usr/bin/env python
# encoding: utf-8
"""
@version: 1.0 Beta
@author: Deepak
@license: MIT Licence
@contact: medgloss@gmail.com
@site: https://www.medgloss.com/
@software: Visual Studio Code
@file: build_search_words.py
"""

from django.core.management.base import BaseCommand
from blog.models import Article, Tag, Category


class Command(BaseCommand):
    help = 'build search words'

    def handle(self, *args, **options):
        datas = set([t.name for t in Tag.objects.all()] +
                    [t.name for t in Category.objects.all()])
        print('\n'.join(datas))
