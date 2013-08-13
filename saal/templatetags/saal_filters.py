# -*- coding: utf-8 -*-
#
# File: admin.py
#
# Copyright (c) 2012 by Interlegis
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
from django import template
from django.utils.translation import ugettext as _

register = template.Library()

@register.filter
def app_doc(app_name):
    try:
        app = __import__(app_name.lower())
        return app.__doc__ or _(u"<h3>Click the title above to access application options</h3>")
    except Exception:
        return _(u"<h3>Click the title above to access application options</h3>")
    
@register.filter
def app_title(app_name):
    try:
        app = __import__(app_name.lower())
        return app.__title__ or _(app_name)
    except Exception:
        return _(app_name)

@register.filter
def app_brief(app_name):
    try:
        app = __import__(app_name.lower())
        return app.__brief__ or _(app_name)
    except Exception:
        return _(app_name)

@register.filter
def app_topics(app_name):
    try:
        app = __import__(app_name.lower())
        topics = app.__topics__ or []
        return "<li>" + "</li><li>".join(topics) + "</li>"
    except Exception:
        return "<li>%s</li>" % _(app_name)