# -*- coding: utf-8 -*-
#
# File: spat.views
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
from django.shortcuts import get_object_or_404
from django.template import Template, Context
from saal.reports import TemplatePdfView
from spat.models import AssetMovement , AssetClass, Asset
from django.views.generic.base import TemplateView

class PrintRegistryTerm(TemplatePdfView):
    pdf_template = 'spat/report/pdf/term_pdf.html'

    def get_context_data(self, **kwargs):
        context = super(PrintRegistryTerm, self).get_context_data(**kwargs)
        movement = get_object_or_404(AssetMovement, pk=kwargs['mov_id'])
        registry = movement.origin
        term = registry.term_model
        term_text = term.term_text
        
        self.pdf_file_name = term.get_term_type_display()
        
        extra_context = {
            "asset_code"           : registry.asset.asset_code,
            "asset_type"           : registry.asset.asset_type.description,
            "asset_description"    : registry.asset.description        if term.term_type != 'C' else registry.old_description,
            "registry_date"        : registry.registry_date,
            "registry_annotation"  : registry.annotation,
            "transfer_from_unit"   : registry.from_unit.name           if term.term_type == 'T'        else None,
            "transfer_to_unit"     : registry.to_unit.name             if term.term_type == 'T'        else None,
            "transfer_from_chief"  : registry.from_chief.name          if term.term_type == 'T'        else None,
            "transfer_to_chief"    : registry.to_chief.name            if term.term_type == 'T'        else None,
            "writedown_cause"      : registry.get_down_cause_display() if term.term_type == 'W'        else None,
            "asset_old_value"      : registry.old_value                if term.term_type in ('C', 'D') else None,
            "asset_old_description": registry.old_description          if term.term_type == 'C'        else None,
            "depreciation_value"   : registry.depreciation_value       if term.term_type == 'D'        else None,
            "asset_new_value"      : registry.new_value                if term.term_type in ('C', 'D') else None,
            "asset_new_description": registry.new_description          if term.term_type == 'C'        else None,}
        
        t = Template(term_text)
        term_text = t.render(Context(extra_context))
        extra_context['term_text'] = term_text
        extra_context['term'] = term
        extra_context['registry'] = registry
        
        context.update(extra_context)
        return context

class CompositionSheetSnippet(TemplateView):
    template_name = 'spat/composition_sheet_snippet.html'
    def get_context_data(self, **kwargs):
        context = super(CompositionSheetSnippet, self).get_context_data(**kwargs)
        today = datetime.date.today()
        sheet = []
        for classe in AssetClass.objects.all():
            sheet_item = {'description': unicode(classe), 'total_asset': 0, 'total_insured': 0}
            for asset in Asset.objects.filter(status='U', asset_type__asset_class=classe):
                sheet_item['total_asset'] += asset.actual_value
                sheet_item['total_insured'] += sum([ins.amount_insured for ins in asset.insurancepolicy_set.filter(
                                                        start_date__lte=today, end_date__gte=today)])
            sheet.append(sheet_item)
        totals = {'total_asset': sum(i['total_asset'] for i in sheet), 'total_insured': sum(i['total_insured'] for i in sheet)}
        context['composition_sheet'] = sheet
        context['sheet_totals'] = totals
        return context