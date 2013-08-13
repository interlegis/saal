# -*- coding: utf-8 -*-
#
# File: /home/sesostris/workspace/saal/smat/filters.py
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
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.db.models import Sum, Q, F

class StockListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _(u'Stock status')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'st'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('z', _(u'Without stock')),
            ('um', _(u'Under minimum')),
            ('om', _(u'Above maximum')),
            ('sp', _(u'Supply point')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Add stock_qty annotate field
        queryset = queryset.annotate(stock=Sum('materialcluster__quantity'))
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value() == 'z':
            return queryset.filter(Q(stock__lte=0) | Q(stock=None))
        elif self.value() == 'um':
            return queryset.filter(Q(stock__lte=F('stock_min')) | Q(stock=None))
        elif self.value() == 'om':
            return queryset.filter(stock__gte=F('stock_max'))
        elif self.value() == 'sp':
            return queryset.filter(Q(stock__lte=F('supply_point')) | Q(stock=None))
