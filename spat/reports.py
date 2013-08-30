# -*- coding: utf-8 -*-
#
# File: spat.reports
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
import datetime
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.forms import forms
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from saal.reports import TabularListView
from spat.models import Inventory, InventoryDetail, WriteDownRegistry, TransferRegistry, DepreciationRegistry, ChangeRegistry
from saal.models import OrganizationalUnit

class InventoryReport(TabularListView):
    app_label = 'spat'
    title = _(u"Asset inventory report")
    page_size = "A4 landscape"
    list_fields = [{'name': 'unit', 'width': '12%', 'label': _('Unit')},
                   {'name': 'asset_code', 'style': 'text-align: right;', 'pdf_style': 'text-align: right;', 'width': '4%', 'label': _('Asset code')},
                   {'name': 'description', 'width': '77%', 'label': _('Description')},
                   {'name': 'value', 'style': 'text-align: right;', 'pdf_style': 'text-align: right;', 'width': '7%', 'label': _('Value')}]

    analitical_groups = [{'group_field': 'value',
                          'totals': [{'field':'unit',
                                      'label':_(u"Total for Organizational Unit %(value)s: %(key)s"),
                                      'function': lambda x,y: x+y }]}]
    
    groups = analitical_groups
    totals = [{'field': 'value', 'label': 'Total inventory: (%s)', 'function': lambda x,y: x+y}]
    
    year_month = forms.CharField(label=_(u"Year month"), max_length=6, min_length=6,
                    help_text=_(u"Format: yyyymm where yyyy is the four digits year and mm is the two-digits month"))
    report_mode = forms.ChoiceField(label=_(u"Report mode"), choices=(('S', 'Synthetic'), ('A', 'Analytical')), 
                    widget=forms.RadioSelect)
    unit = forms.ModelChoiceField(queryset=OrganizationalUnit.objects.all(), required=False, empty_label=_(u"All units"),
                    label=_("Organizational unit"))

    def get_queryset(self):
        self.form_load_data()
        if not self.is_valid():
            return None
        
        year_month = self.cleaned_data['year_month']
        report_mode = self.cleaned_data['report_mode']
        unit = self.cleaned_data['unit']

        result = []
        inventory = get_object_or_404(Inventory, year_month=year_month)

        detail_set = inventory.inventorydetail_set.all()
        if unit is not None:
            detail_set = inventory.inventorydetail_set.filter(unit=unit)
        
        if report_mode == 'A':
            self.groups = self.analitical_groups
            for detail in detail_set:
                result.append({'unit': detail.unit.name, 'asset_code': detail.asset.asset_code,'description': detail.asset_description,
                               'value': detail.asset_value})
        else:
            self.groups = []
            for unit_rec in detail_set.values('unit__name').annotate(total_value=Sum('asset_value')):
                result.append({'unit': unit_rec['unit__name'], 'asset_code': '****', 'description': unit_rec['unit__name'],
                               'value': unit_rec['total_value'], })
        
        return result

class SheetEvolutionReport(TabularListView):
    title = _(u"Sheet evolution report")
    app_label = 'spat'
    page_size = 'A4 landscape'
    year_month_start = forms.CharField(label=_(u"Start year/month"), min_length=6, max_length=6)
    year_month_end = forms.CharField(label=_(u"End year/month"), min_length=6, max_length=6)
    unit = forms.ModelChoiceField(queryset=OrganizationalUnit.objects.all(), required=False, empty_label=_(u"All units"),
                    label=_("Organizational unit"))
    
    def get_queryset(self):
        self.form_load_data()
        if not self.is_valid():
            return None
        
        start = self.cleaned_data['year_month_start']
        end = self.cleaned_data['year_month_end']
        unit = self.cleaned_data['unit']
        
        return self.get_data(start=start, end=end, unit=unit)
    
    def get_data(self, start, end, unit=None):
        start_year = int(start[:4])
        start_month = int(start[4:])
        end_year = int(end[:4])
        end_month = int(end[4:])
        
        stt = datetime.datetime.strptime("%s-%s-01" % (start_year, start_month,), '%Y-%m-%d')
        ett = datetime.datetime.strptime("%s-%s-01" % (end_year, end_month,), '%Y-%m-%d')
        
        if stt >= ett:
            raise Exception("Start date must be less than end date.")
        
        months = []
        queryset = []
        clear_line = {'unit_id': None, 'unit_name': None, }
        
        while stt <= ett:
            year_month = "%04d%02d" % (start_year, start_month)
            months.append(year_month)
            clear_line[year_month] = 0
            start_month += 1
            if start_month > 12:
                start_year += 1
                start_month = 1
            stt = datetime.datetime.strptime("%s-%s-01" % (start_year, start_month,), '%Y-%m-%d')

        if unit is None:
            unit_set = OrganizationalUnit.objects.all()
        else:
            unit_set = [unit]
        
        for unit in unit_set:
            unit_line = clear_line.copy()
            unit_line['unit_id'] = unit.id
            unit_line['unit_name'] = unit.name
            queryset.append(unit_line)
        
        for detail in InventoryDetail.objects.filter(inventory_id__in=months, unit__in=unit_set):
            unit_line = [r for r in queryset if r['unit_id']==detail.unit_id][0]
            unit_line[detail.inventory_id] += detail.asset_value
            
        self.list_fields = ['unit_name'] + [{'name': m, 'style': 'text-align:right;', 'pdf_style': 'text-align:right;',
            'label': _("%(year)s-%(month)s" % {'year': m[:4], 'month': m[4:]})} for m in months]
        self.totals = [{'field': m, 'label': '%s', 'function': lambda x,y: x+y} for m in months]
        self.get_list_fields() # Force list field processing

        return queryset

class WritedownByCauseReport(TabularListView):
    model = WriteDownRegistry
    page_size = 'A4 landscape'
    title = _(u"Asset writed down by cause report")
    list_fields = [{'name': 'registry_date', 'label': 'Writedown date'}, 'asset__asset_code', 'asset__description',
                   'asset__acquisition_value', 'asset__actual_value', {'name': 'get_down_cause_display','label': 'Writedown cause'}]
    registry_date__gte = forms.DateField(label=_(u"Start date"))
    registry_date__lte = forms.DateField(label=_(u"End date"))
    down_cause = forms.ChoiceField(label=_(u"Writedown cause"), required=False, 
                              choices=[('', _('Any cause'))] + list(WriteDownRegistry.DOWN_CAUSE_CHOICES))

class MovementByPeriodReport(TabularListView):
    page_size = 'A4 landscape'
    title = _(u"Movements by period report")
    app_label = 'spat'
    MOVEMENT_TYPE_CHOICES = (
        ('T', _(u'Transfer registry')),
        ('D', _(u'Depreciation registry')),
        ('C', _(u'Change registry')),)
    movement_type = forms.ChoiceField(label=_(u"Movement type"), choices=MOVEMENT_TYPE_CHOICES)
    start_date = forms.DateField(label=_(u"Start date"))
    end_date = forms.DateField(label=_(u"End date"))
    
    def get_queryset(self):
        self.form_load_data()
        if not self.is_valid():
            return None
        
        movement_type = self.cleaned_data['movement_type']
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        
        queryset = []
        
        if movement_type == 'T':
            self.model = TransferRegistry
            queryset = TransferRegistry.objects.filter(registry_date__gte=start_date, registry_date__lte=end_date)
            self.list_fields = ['registry_date', 'asset__asset_code', 'asset__description', 'from_unit', 'to_unit',] 
        elif movement_type == 'D':
            self.model = DepreciationRegistry
            queryset = DepreciationRegistry.objects.filter(registry_date__gte=start_date, registry_date__lte=end_date)
            self.list_fields = ['registry_date', 'asset__asset_code', 'asset__description', 'old_value', 'depreciation_value',
                                'new_value',]
        elif movement_type == 'C':
            self.model = ChangeRegistry
            queryset = ChangeRegistry.objects.filter(registry_date__gte=start_date, registry_date__lte=end_date)
            self.list_fields = ['registry_date', 'asset__asset_code', 'old_description', 'old_value', 'new_description', 
                                'new_value',]
        self.get_list_fields()
        return queryset
        
