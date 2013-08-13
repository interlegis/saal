# -*- coding: utf-8 -*-
#
# File: tree_menu_tags_extend.py
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
from treemenus.models import Menu

register = template.Library()

@register.filter
def menu_exists(menu_name):
    ''' Returns True if 'menu_name' is a valid menu name.
        Usage:
            {% if 'your_menu_name'|menu_exists %}
                {% do anything %}
            {% endif %}'''
    return Menu.objects.filter(name=menu_name).exists()