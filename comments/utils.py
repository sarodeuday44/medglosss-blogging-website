#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0 Beta
@author: Deepak
@license: MIT Licence
@contact: medgloss@gmail.com
@site: https://www.medgloss.com/
@software: Visual Studio Code
@file: utils.py
"""

from Medgloss.utils import send_email
from Medgloss.utils import get_current_site
import logging

logger = logging.getLogger(__name__)


def send_comment_email(comment):
    site = get_current_site().domain
    subject = 'Thank you for posting your comment !'
    article_url = "https://{site}{path}".format(
        site=site, path=comment.article.get_absolute_url())
    html_content = """
                   <p>Thank you very much for commenting on this site.</p>
                   you can visit
                   <a href="%s" rel="bookmark">%s</a>
                   Come and see your review，
                   Thank you again！
                   <br />
                   If the above link doesn't open，Please copy this link to your browser.
                   %s
                   """ % (article_url, comment.article.title, article_url)
    tomail = comment.author.email
    send_email([tomail], subject, html_content)
    try:
        if comment.parent_comment:
            html_content = """
                    You are <a href="%s" rel="bookmark">%s</a> comment of <br/> %s <br/> Received a reply. Go see it.
                    <br/>
                    If the above link doesn't open, copy this link to your browser.
                    %s
                    """ % (article_url, comment.article.title, comment.parent_comment.body, article_url)
            tomail = comment.parent_comment.author.email
            send_email([tomail], subject, html_content)
    except Exception as e:
        logger.error(e)
