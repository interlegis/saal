# -*- coding: utf-8 -*-
#
# File: spat.__init__
#
# Copyright (c) 2013 by Interlegis
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
from django.utils.translation import ugettext as _
__doc__ = _( 
u'''
<h3>Patrimonial System</h3>
<p>Controls the assets and their movements in Legislative house.</p>
<ul>
    <li>Table maintenance</li>
    <li>Asset registration</li>
    <li>Insurance policies</li>
    <li>Transfer, depreciation, changes and writedown registries</li>
    <li>Inventories and Asset reports</li>
</ul>
''')

__title__ = _(u'Patrimonial System')
__brief__ = _(u'Controls the assets and their movements in Legislative house.')
__topics__ = (_(u'Table maintenance'),
              _(u'Asset registration'),
              _(u'Insurance policies'),
              _(u'Transfer, depreciation, changes and writedown registries'),)