# -*- coding: utf-8 -*-
#
# File: urls.py
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
from django.conf.urls import patterns, url
from spat.views import PrintRegistryTerm, CompositionSheetSnippet
from spat.reports import InventoryReport, SheetEvolutionReport, WritedownByCauseReport, MovementByPeriodReport

urlpatterns = patterns('',
    # View urls
    url(r'^printterm/(?P<mov_id>\d+)', PrintRegistryTerm.as_view(), name="printterm"),
    url(r'^compositionsheetsnippet/', CompositionSheetSnippet.as_view(), name="compositionsheetsnippet"),
    # Report urls
    url(r'^inventoryreport', InventoryReport.as_view(), name="inventoryreport"),
    url(r'^sheetevolutionreport', SheetEvolutionReport.as_view(), name="sheetevolutionreport"),
    url(r'^writedownbycausereport', WritedownByCauseReport.as_view(), name="writedownbycausereport"),
    url(r'^movementbyperiodreport', MovementByPeriodReport.as_view(), name="movementbyperiodreport"),
    # Chart images
    url(r'^galsheetevolution', 'spat.charts.galSheetEvolution', name='galsheetevolution'),
)