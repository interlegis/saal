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
from django.utils.translation import ugettext_lazy as _
import cairosvg
import pygal
from pygal.style import LightStyle
from datetime import datetime
from django.http.response import HttpResponse
from spat.reports import SheetEvolutionReport

def galSheetEvolution(request):
    ''' Plots a line chart showing the material cost by Organizational Units'''
    width = int(request.GET.get('w', '400'))
    height = int(request.GET.get('h', '240'))
    end_month = request.GET.get('end_month', datetime.today().strftime('%Y%m'))
    if 'start_month' in request.GET:
        start_month = request.GET.get('start_month', datetime.today().strftime('%Y%m'))
    else: # Calcs 12 months ago
        if end_month[4:] == '12':
            start_month = end_month[:4] + '01'
        else:
            start_month = "%04d%02d" % (int(end_month[:4]) - 1, int(end_month[4:]) + 1,)
    
    ser = SheetEvolutionReport()
    data = ser.get_data(start=start_month, end=end_month)
    chart = pygal.Line(width=width, height=height, style=LightStyle, title_font_size=12, x_label_rotation=20, legend_at_bottom=True)
    chart.title = unicode(_(u'From %(start_year)s-%(start_month)s to %(end_year)s-%(end_month)s'% {'start_year': start_month[:4],
                        'start_month': start_month[4:], 'end_year': end_month[:4], 'end_month': end_month[4:]}))
    field_names = [f['name'] for f in ser.get_list_fields()]
    field_labels = [unicode(f['label']) for f in ser.get_list_fields()]
    chart.x_labels = field_labels[1:]
    
    for row in data[1:]:
        sequence = [float(row[f]) for f in field_names[1:]]
        chart.add(row['unit_name'], sequence)
              
    svg = chart.render()
    png = cairosvg.svg2png(svg)
        
    return HttpResponse(png, 'image/png')