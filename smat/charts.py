# -*- coding: utf-8 -*-
#
# File: smat.charts
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
import cairosvg
import pygal
from pygal.style import LightStyle
from datetime import datetime
from smat.models import Request, MaterialCluster, PurchaseInvoice
from django.http.response import HttpResponse
from django.utils.datastructures import SortedDict

def galYearCostByOU(request):
    ''' Plots a pie chart showing the material cost by Organizational Units'''
    width = int(request.GET.get('w', '400'))
    height = int(request.GET.get('h', '240'))
    end_date = datetime.strptime(request.GET.get('end_date', datetime.today().strftime('%Y-%m-%d')), '%Y-%m-%d')
    if 'start_date' in request.GET:
        start_date = datetime.strptime(request.GET.get('start_date', datetime.today().strftime('%Y-%m-%d')), '%Y-%m-%d')
    else: # Calcs 12 months ago
        if end_date.month == 12:
            start_date = datetime(end_date.year, 1, 1)
        else:
            start_date = datetime(end_date.year - 1, end_date.month + 1, 1)
    
    series = {}
    
    for req in Request.objects.filter(complied_date__gt=start_date, complied_date__lte=end_date):
        unit = req.request_unit.name
        if unit not in series:
            series[unit] = 0
        series[unit] += req.total_cost
              
    chart = pygal.Pie(width=width, height=height, style=LightStyle, title_font_size=12)
    chart.title = _(u'From %(startdate)s to %(enddate)s') % {'startdate': start_date.strftime('%d-%m-%Y'), 'enddate': end_date.strftime('%d-%m-%Y')}
    
    for (key, value) in series.iteritems():
        chart.add(key, float(value))
        
    svg = chart.render()
    png = cairosvg.svg2png(svg)
        
    return HttpResponse(png, 'image/png')

def galStockByCategory(request):
    ''' Plots a pie chart showing the material cost by Organizational Units'''
    width = int(request.GET.get('w', '400'))
    height = int(request.GET.get('h', '240'))
    
    series = {}
    
    for cl in MaterialCluster.objects.filter(quantity__gt=0):
        classe = cl.material.material_class.description
        if classe not in series:
            series[classe] = 0
        series[classe] += cl.total_cost
              
    chart = pygal.Pie(width=width, height=height, style=LightStyle, title_font_size=12)
    chart.title = _(u'Actual stock')
    
    for (key, value) in series.iteritems():
        chart.add(key, float(value))
        
    svg = chart.render()
    png = cairosvg.svg2png(svg)
        
    return HttpResponse(png, 'image/png')

def galYearPurchase(request):
    ''' Plots a pie chart showing the material cost by Organizational Units'''
    width = int(request.GET.get('w', '400'))
    height = int(request.GET.get('h', '240'))
    end_date = datetime.strptime(request.GET.get('end_date', datetime.today().strftime('%Y-%m-%d')), '%Y-%m-%d')
    if 'start_date' in request.GET:
        start_date = datetime.strptime(request.GET.get('start_date', datetime.today().strftime('%Y-%m-%d')), '%Y-%m-%d')
    else: # Calcs 12 months ago
        if end_date.month == 12:
            start_date = datetime(end_date.year, 1, 1)
        else:
            start_date = datetime(end_date.year - 1, end_date.month + 1, 1)
        
    year = start_date.year
    month = start_date.month 
    
    data = SortedDict()
    
    while (datetime(year, month, 1) < end_date):
        data[datetime(year, month, 1).strftime('%m-%Y')] = 0
        month += 1
        if month > 12:
            year += 1
            month = 1
    
    for inv in PurchaseInvoice.objects.filter(input_date__gt=start_date, input_date__lte=end_date).order_by('input_date'):
        month_year = inv.input_date.strftime('%m-%Y')
        data[month_year] += inv.total_cost
              
    chart = pygal.Line(width=width, height=height, style=LightStyle, x_label_rotation=30, show_legend=False, interpolate='cubic', title_font_size=12)
    chart.title = _(u'From %(startdate)s to %(enddate)s') % {'startdate': start_date.strftime('%d-%m-%Y'), 'enddate': end_date.strftime('%d-%m-%Y')}
    chart.x_labels = data.keys()
    chart.add(_(u'Purchases'), map(float, data.values()))
    
    svg = chart.render()
    png = cairosvg.svg2png(svg)
        
    return HttpResponse(png, 'image/png')
