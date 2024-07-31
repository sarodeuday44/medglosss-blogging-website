#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0 Beta
@author: Deepak
@license: MIT Licence
@contact: medgloss@gmail.com
@site: https://www.medgloss.com/
@software: Visual Studio COde
@file: urls.py
"""

from django.conf.urls import url
from django.contrib.auth import views as auth_view
from django.urls import path
from . import views
from .forms import LoginForm

app_name = "accounts"

urlpatterns = [url(r'^login/$',
                   views.LoginView.as_view(success_url='/'),
                   name='login',
                   kwargs={'authentication_form': LoginForm}),
               url(r'^register/$',
                   views.RegisterView.as_view(success_url="/"),
                   name='register'),
               url(r'^logout/$',
                   views.LogoutView.as_view(),
                   name='logout'),
               path(r'account/result.html',
                    views.account_result,
                    name='result')]
