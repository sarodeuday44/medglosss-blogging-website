#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0 Beta
@author: Deepak
@license: MIT Licence
@contact: medgloss@gmail.com
@site: https://www.medgloss.com/
@software: Visual Studio Code
@file: feed.py
"""
# Python3 program to extract all the numbers from a string
from datetime import datetime
from django.contrib.auth import get_user_model
from Medgloss.utils import CommonMarkdown
from django.utils.feedgenerator import Rss201rev2Feed
from django.conf import settings
from blog.models import Article
from django.contrib.syndication.views import Feed


class MedglossFeed(Feed):
    feed_type = Rss201rev2Feed

    description = 'Medgloss Feed'
    title = "Medgloss Feed"
    link = "/feed/"

    def author_name(self):
        return get_user_model().objects.first().nickname

    def author_link(self):
        return get_user_model().objects.first().get_absolute_url()

    def items(self):
        return Article.objects.filter(type='a', status='p').order_by('-pub_time')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return CommonMarkdown.get_markdown(item.body)

    def feed_copyright(self):
        now = datetime.now()
        return "Copyright© {year} Medgloss".format(year=now.year)

    def item_link(self, item):
        return item.get_absolute_url()

    def item_guid(self, item):
        return
