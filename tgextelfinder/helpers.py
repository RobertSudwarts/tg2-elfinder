# -*- coding: utf-8 -*-

"""WebHelpers used in tgext.elfinder."""

#from webhelpers import date, feedgenerator, html, number, misc, text
from markupsafe import Markup

def bold(text):
    return Markup('<strong>%s</strong>' % text)