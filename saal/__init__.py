# -*- coding: utf-8 -*-
# File: saal.__init__
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
<h3>SAAL base System</h3>
<p>Base tables for system SAAL.</p>
<ul>
    <li>Political organization (states & cities)</li> 
    <li>Organizational structure</li>
    <li>Supplier base table</li>
</ul>
''')
 
__title__ = _(u'SAAL base System')
__brief__ = _(u'Base tables for system SAAL.')
__topics__ = (_(u'Political organization (states & cities)'),
              _(u'Organizational structure'),
              _(u'Supplier base table'),)