#!/usr/bin/env python
# encoding: utf-8
"""
@version: 1.0 Beta
@author: Deepak
@license: MIT Licence
@contact: medgloss@gmail.com
@site: https://www.medgloss.com/
@software: Visual Studio Code
@file: build_index.py
"""

from blog.documents import ElapsedTimeDocument, ArticleDocumentManager

from django.core.management.base import BaseCommand
from blog.models import Article


class Command(BaseCommand):
    help = 'build search index'

    def handle(self, *args, **options):
        manager = ArticleDocumentManager()
        manager.delete_index()
        manager.rebuild()

        manager = ElapsedTimeDocument()
        manager.init()
