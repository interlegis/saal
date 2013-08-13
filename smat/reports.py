# -*- coding: utf-8 -*-
#
# smat.reports
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
from django.db.models import Q
from django.contrib.admin.forms import forms
from saal.reports import TabularListView
from smat.models import MaterialClass, Material, RequestItem, Request, PurchaseItem
from saal.models import OrganizationalUnit

class PurchaseReport(TabularListView):
    title = _(u'Purchases by period')
    model = PurchaseItem
    list_fields = [{'name': 'invoice__input_date', 'label': _(u'Purchase data')},
                  {'name': 'material__material_class'},
                  {'name': 'material__item_code'},
                  {'name': 'material__description', 'label': _(u'Material')},
                  {'name': 'material__measure_unit'},
                  {'name': 'quantity', 'style': 'text-align: right;', 'pdf_style': 'text-align: right;'},
                  {'name': 'unit_cost', 'style': 'text-align: right;', 'pdf_style': 'text-align: right;'},
                  {'name': 'total_cost', 'style': 'text-align: right;', 'pdf_style': 'text-align: right;'}]
    totals = [{'field': 'total_cost', 'label': _(u'Sum of total cost: %s'), 'function': lambda x,y: x+y},]
    groups = [{'group_field': 'material__material_class', 'totals': [{'field': 'total_cost', 'label': _(u'Total cost for %(key)s: %(value)s'), 'function': lambda x,y: x+y}]}]

    start_date = forms.DateField(label=_(u'Start date'))
    end_date = forms.DateField(label=_(u'End date'))
    
    def filter(self, queryset):
        if not self.is_valid():
            return None
        
        return queryset.filter(invoice__input_date__gte=self.cleaned_data['start_date']) \
                            .filter(invoice__input_date__lte=self.cleaned_data['end_date']) \
                            .order_by('material__material_class', 'material')
        
class TotalCostReport(TabularListView):
    title = _(u'Total cost by unit')
    app_label = 'smat'
    list_fields = [{'name': 'account_code', 'label': _(u'Account code')},
                   {'name': 'account_name', 'label': _(u'Account name')},
                   {'name': 'total_cost', 'label': _(u'Total cost'), 'style': 'text-align: right;', 'pdf_style': 'text-align: right;'},]
    totals = [{'field': 'total_cost', 'label': _(u'Sum of total cost: %s'), 'function': lambda x,y: x+y},]

    start_date = forms.DateField(label=_(u'Start date'))
    end_date = forms.DateField(label=_(u'End date'))
    
    def get_queryset(self):
        self.form_load_data()
        if not self.is_valid():
            return None
        
        requests = Request.objects.filter(complied_date__gte=self.cleaned_data['start_date']) \
                                    .filter(complied_date__lte=self.cleaned_data['end_date']) \
                                    .order_by('request_unit')
        if not requests.exists():
            return None

        queryset = []
        last_unit = None
        row = {'account_code': requests[0].request_unit.account_code,
               'account_name': requests[0].request_unit.name,
               'total_cost': 0}
        
        for req in requests:
            if last_unit is None:
                last_unit = req.request_unit
            if last_unit != req.request_unit:
                last_unit = req.request_unit
                queryset.append(row)
                row = {'account_code': req.request_unit.account_code,
                       'account_name': req.request_unit.name,
                       'total_cost': 0}
            row['total_cost'] += req.total_cost
        queryset.append(row)
        
        return queryset
    
class RequestReport(TabularListView):
    model = RequestItem
    title = _(u"Requests by unit")
    list_fields = [{'name': 'request__complied_date'},
                   {'name': 'request__request_unit'},
                   {'name': 'material__item_code'},
                   {'name': 'material__description'},
                   {'name': 'material__measure_unit'},
                   {'name': 'total_cost', 'style': 'text-align: right;', 'pdf_style': 'text-align: right;'},]
    totals = [{'field': 'total_cost', 'label': _(u'Sum of total cost: %s'), 'function': lambda x,y: x+y},]
    groups = [{'group_field': 'request__request_unit', 'totals': [{'field': 'total_cost', 'label': _(u'Total cost for %(key)s: %(value)s'), 'function': lambda x,y: x+y}]}]
    
    request_unit = forms.ModelChoiceField(queryset=OrganizationalUnit.objects.all(), required=False, empty_label=_(u'All units'))
    start_date = forms.DateField(label=_(u'Start date'))
    end_date = forms.DateField(label=_(u'End date'))
    
    def filter(self, queryset):
        if not self.is_valid():
            return None
        
        if self.cleaned_data['request_unit']:
            queryset = queryset.filter(request__request_unit=self.cleaned_data['request_unit'])
            
        queryset = queryset.filter(request__complied_date__gte=self.cleaned_data['start_date']) \
                           .filter(request__complied_date__lte=self.cleaned_data['end_date']) \
                           .filter(request__request_status='A')
        queryset = queryset.order_by('request__request_unit', 'request__complied_date', 'material')

        return queryset
    
class InventoryReport(TabularListView):
    app_label = 'smat'
    page_size = "A4 landscape"
    title = _(u"Inventory report")
    template_name = 'smat/reports/inventory_report.html'
    template_name_pdf = 'smat/reports/inventory_report_pdf.html'
    total = {'before': 0, 'input': 0, 'output': 0, 'after': 0}

    material_class = forms.ModelChoiceField(label=_(u'Material class'), queryset=MaterialClass.objects.all(), required=False, empty_label=_(u'All classes'))
    start_date = forms.DateField(label=_(u'Start date'))
    end_date = forms.DateField(label=_(u'End date'))

    def get_queryset(self):
        self.form_load_data()
        if not self.is_valid():
            return None
        
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        
        result = []
        self.total = {'before': 0, 'input': 0, 'output': 0, 'after': 0}
        materials = Material.objects.all().order_by('material_class', 'description')

        if self.cleaned_data['material_class']  is not None:
            materials = materials.filter(material_class=self.cleaned_data['material_class'])
            
        last_mc = None
        mc_total = {'before': 0, 'input': 0, 'output': 0, 'after': 0}
        
        for m in materials:
            if last_mc is None:
                last_mc = m.material_class
            
            if last_mc != m.material_class:
                result.append({'group_description': _(u'Totals for %s') % last_mc, 'group_total': mc_total.copy()})
                mc_total = {'before': 0, 'input': 0, 'output': 0, 'after': 0}
                last_mc = m.material_class

            row = {'item_code': m.item_code, 'description': m.description, 'measure_unit': m.measure_unit} 
            clusters = m.materialcluster_set
            clusters = clusters.exclude(Q(creation_date__lt=start_date) & Q(last_change__lt=end_date) & Q(quantity__lte=0))
            clusters = clusters.exclude(creation_date__gt=end_date)
            movements = None 
            for cl in clusters.order_by('creation_date'):
                movs = cl.materialmovement_set.exclude(mov_date__lt=start_date).exclude(mov_date__gt=end_date)
                if movements is None:
                    movements = movs
                else:
                    movements = movements | movs
            if movements is not None:
                for m in movements.order_by('mov_date'):
                    if 'physical' not in row:
                        row['physical'] = {'before': m.qty_before_mov, 'input': 0, 'output': 0, 'after': m.qty_before_mov}  
                        row['financial'] = {'before': m.qty_before_mov * m.unit_cost, 'input': 0, 'output': 0, 'after': m.qty_before_mov * m.unit_cost}
                        self.total['before'] += m.qty_before_mov * m.unit_cost
                        self.total['after'] += m.qty_before_mov * m.unit_cost
                        mc_total['before'] += m.qty_before_mov * m.unit_cost
                        mc_total['after'] += m.qty_before_mov * m.unit_cost
                    if m.type == 'E':
                        row['physical']['input'] += m.quantity
                        row['physical']['after'] += m.quantity
                        row['financial']['input'] += m.quantity * m.unit_cost
                        row['financial']['after'] += m.quantity * m.unit_cost
                        self.total['input'] += m.quantity * m.unit_cost
                        self.total['after'] += m.quantity * m.unit_cost
                        mc_total['input'] += m.quantity * m.unit_cost
                        mc_total['after'] += m.quantity * m.unit_cost
                    else:
                        row['physical']['output'] += m.quantity
                        row['physical']['after'] -= m.quantity
                        row['financial']['output'] += m.quantity * m.unit_cost
                        row['financial']['after'] -= m.quantity * m.unit_cost
                        self.total['output'] += m.quantity * m.unit_cost
                        self.total['after'] -= m.quantity * m.unit_cost
                        mc_total['output'] += m.quantity * m.unit_cost
                        mc_total['after'] -= m.quantity * m.unit_cost
                if 'physical' in row:
                    result.append(row)

        result.append({'group_description': _(u'Totals for %s') % last_mc, 'group_total': mc_total.copy()})

        return result