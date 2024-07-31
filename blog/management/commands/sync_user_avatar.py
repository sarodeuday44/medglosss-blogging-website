#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0 Beta
@author: Deepak
@license: MIT Licence
@contact: medgloss@gmail.com
@site: https://www.medgloss.com/
@software: Visual Studio Code
@file: sync_user_avatar.py
"""

from django.core.management.base import BaseCommand
from oauth.models import OAuthUser
from Medgloss.utils import save_user_avatar


class Command(BaseCommand):
    help = 'sync user avatar'

    def handle(self, *args, **options):
        users = OAuthUser.objects.filter(picture__isnull=False).exclude(
            picture__istartswith='https://resource.medgloss.com').all()
        self.stdout.write(
            'Start sync {count} user avatar'.format(count=len(users)))
        for u in users:
            self.stdout.write(
                'Start synchronization: {id}'.format(id=u.nikename))
            url = u.picture
            url = save_user_avatar(url)
            if url:
                self.stdout.write(
                    'End synchronization:{id}.url:{url}'.format(
                        id=u.nikename, url=url))
                u.picture = url
                u.save()
        self.stdout.write('End synchronization')
