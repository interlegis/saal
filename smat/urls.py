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
from smat.reports import InventoryReport, RequestReport, TotalCostReport, PurchaseReport

urlpatterns = patterns('',
    # Report urls
    url(r'^inventoryreport', InventoryReport.as_view(), name="inventoryreport"),
    url(r'^requestreport', RequestReport.as_view(), name="requestreport"),
    url(r'^totalcostreport', TotalCostReport.as_view(), name="totalcostreport"),
    url(r'^purchasereport', PurchaseReport.as_view(), name="purchasereport"),
    # Graphics & chart urls
    url(r'^galcostbyou', 'smat.charts.galYearCostByOU', name='galYearCostByOU'),
    url(r'^galpurchase', 'smat.charts.galYearPurchase', name='galYearPurchase'),
    url(r'^galstockbycategory', 'smat.charts.galStockByCategory', name='galStockByCategory'),
)