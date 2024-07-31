#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0 Beta
@author: Deepak
@license: MIT Licence
@contact: medgloss@gmail.com
@site: https://www.medgloss.com/
@software: Visual Studio Code
@file: urls.py
"""

from django.urls import path
from . import views

app_name = "comments"
urlpatterns = [
    # url(r'^po456stcomment/(?P<article_id>\d+)$', views.CommentPostView.as_view(), name='postcomment'),
    path(
        'article/<int:article_id>/postcomment',
        views.CommentPostView.as_view(),
        name='postcomment'),
]
