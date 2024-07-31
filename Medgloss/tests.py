#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0 Beta
@author: Deepak
@license: MIT Licence
@contact: medgloss@gmail.com
@site: https://www.medgloss.com/
@software: Visual Studio Code
@file: tests.py

"""

from django.test import Client, RequestFactory, TestCase
from blog.models import Article, Category, Tag
from django.contrib.auth import get_user_model
from Medgloss.utils import get_current_site
from django.urls import reverse
import datetime
from Medgloss.utils import *


class MedglossTest(TestCase):
    def setUp(self):
        pass

    def test_utils(self):
        md5 = get_md5('test')
        self.assertIsNotNone(md5)
        c = CommonMarkdown.get_markdown('''
        # Title1

        ```python
        import os
        ```

        [url](https://www.medgloss.com)

        [ddd](http://www.baidu.com)


        ''')
        self.assertIsNotNone(c)
        d = {
            'd': 'key1',
            'd2': 'key2'
        }
        data = parse_dict_to_url(d)
        self.assertIsNotNone(data)
        render = BlogMarkDownRenderer()
        s = render.autolink('http://www.baidu.com')
        self.assertTrue(s.find('nofollow') > 0)
        s = render.link('http://www.baidu.com', 'test', 'test')
        self.assertTrue(s.find('nofollow') > 0)
