# -*- coding: utf-8 -*-
#
# File: spat.admin
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
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from saal.reports import ModelAdminPdf
from spat.models import AssetClass, AssetCatalog, Asset, AssetMovement, TransferRegistry, WriteDownRegistry, DepreciationRegistry,\
    ChangeRegistry, TermModel, Inventory, InventoryDetail, InsurancePolicy

class AssetInsureFilter(admin.SimpleListFilter):
    title = _(u"Insure policy")
    parameter_name = 'insured'
    
    def lookups(self, request, model_admin):
        return (
            ('1', _(u"Insured")),
            ('0', _(u"Not insured"),)
        )
        
    def queryset(self, request, queryset):
        today = datetime.date.today()
        if self.value() == "0":
            queryset = queryset.exclude(insurancepolicy__start_date__lte=today, insurancepolicy__end_date__gte=today)
        elif self.value() == "1":
            queryset = queryset.filter(insurancepolicy__start_date__lte=today, insurancepolicy__end_date__gte=today)
        return queryset
    
class AssetClassAdmin(ModelAdminPdf):
    list_display = ('sign', 'description',)
    search_fields = ('sign', 'description',)
    
class AssetCatalogAdmin(ModelAdminPdf):
    list_display = ('item_code', 'asset_class', 'description',)
    list_filter = ('asset_class',)
    search_fields = ('item_code', 'asset_class__sign', 'asset_class__description', 'description',)

class AssetMovementInline(admin.TabularInline):
    model = AssetMovement
    extra = 0
    max_num = 0
    can_delete = False
    fields = ('mov_date', 'origin', 'annotation', 'get_print_term_url', )
    readonly_fields = fields
    verbose_name, verbose_name_plural = _(u"Asset movement history"), _(u"Asset movements history")
    
    def get_print_term_url(self, obj):
        link = _(u'<a href="%s">Print term</a>' % reverse('spat:printterm', kwargs={'mov_id': obj.pk}))
        return link 
    get_print_term_url.short_description = _(u"Print term")
    get_print_term_url.allow_tags = True

class AbstractRegistryInline(admin.StackedInline):
    extra = 1
    max_num = 1
    can_delete = False
    def queryset(self, request):
        return self.model.objects.get_empty_query_set()
    
class TransferRegistryInline(AbstractRegistryInline):
    model = TransferRegistry
    fields = ('term_model', 'to_unit', 'annotation', )
    verbose_name, verbose_name_plural = _(u"Add new transfer registry"), _(u"Add new transfer registries")

class WriteDownRegistryInline(AbstractRegistryInline):
    model = WriteDownRegistry
    fields = ('term_model', 'down_cause', 'annotation', )
    verbose_name, verbose_name_plural = _(u"Add new writedown registry"), _(u"Add new writedown registries")

class DepreciationRegistryInline(AbstractRegistryInline):
    model = DepreciationRegistry
    fields = ('term_model', 'depreciation_value', 'annotation', )
    verbose_name, verbose_name_plural = _(u"Add new depreciation registry"), _(u"Add new depreciation registries")
    
class ChangeRegistryInline(AbstractRegistryInline):
    model = ChangeRegistry
    fields = ('term_model', 'new_value', 'new_description', 'annotation', )
    verbose_name, verbose_name_plural = _(u"Add new change registry"), _(u"Add new change registries")
        
class InsurancePolicyInline(admin.TabularInline):
    model = InsurancePolicy
    fields = ('policy_id', 'start_date', 'end_date', 'insurance_premium', 'amount_insured', 'deductible_credits', 'annotation', )
        
class AssetAdmin(ModelAdminPdf):
    fields = ('asset_code', 'asset_type', 'description', 'actual_place', 'classification_code', 'acquisition_type', 'acquisition_doc_type',
              'acquisition_doc_num', 'supplier', 'acquisition_date', 'acquisition_value', 'actual_value', 'status',)
    readonly_fields = ['status',]
    list_display = ('asset_code', 'description', 'actual_place', 'actual_value', 'status',)
    list_filter = ('status', 'asset_type__asset_class', 'asset_type', 'actual_place', AssetInsureFilter,)
    search_fields = ('asset_code', 'description', 'asset_type__item_code', 'asset_type__asset_class__sign', 
                   'asset_type__asset_class__description', 'asset_type__description',)
    base_inlines = (InsurancePolicyInline, AssetMovementInline, TransferRegistryInline, DepreciationRegistryInline, ChangeRegistryInline,
               WriteDownRegistryInline, )
    inlines = base_inlines

    def get_inline_instances(self, request, obj=None):
        if obj is not None and obj.status == 'D':
            self.inlines = (InsurancePolicyInline, AssetMovementInline, )
        else:
            self.inlines = self.base_inlines
        return super(AssetAdmin, self).get_inline_instances(request, obj)  
    
    def get_readonly_fields(self, request, obj=None):
        if obj is None or obj.pk is None:
            return self.readonly_fields
        else:
            return self.readonly_fields + ['actual_place', 'actual_value']

class TermModelAdmin(admin.ModelAdmin):
    fields = ('term_type', 'model_name', 'is_active', 'term_text',)
    list_display = ('term_type', 'model_name', 'is_active',)
    list_filter = ('term_type', 'is_active',)
    search_fields = ('model_name',)
    
class InventoryDetailInline(admin.TabularInline):
    model = InventoryDetail
    fields = ('unit', 'get_asset_code', 'asset_description', 'asset_value',)
    readonly_fields = fields
    extra = 0
    max_num = 0
    can_delete = False
    
    def get_asset_code(self, obj):
        return obj.asset.asset_code
    get_asset_code.short_description = _(u"Asset code")
    
class InventoryAdmin(admin.ModelAdmin):
    fields = ('year_month', 'generation_date', 'total_value',)
    readonly_fields = ('generation_date', 'total_value', )
    list_display = ('year_month', 'generation_date', 'total_value',)
    search_fields = ('year_month',)
    date_hierarchy = 'hidden_year_month_fstday'
    inlines = (InventoryDetailInline,)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.fields
        return self.readonly_fields

class InsurancePolicyAdmin(ModelAdminPdf):
    page_size = 'A4 landscape'
    fields = ('policy_id', 'asset_insured', 'start_date', 'end_date', 'insurance_premium', 'amount_insured', 'deductible_credits',
              'annotation',)
    raw_id_fields = ('asset_insured',)
    list_display = ('policy_id','get_asset_code', 'get_asset_place', 'start_date', 'end_date', 'insurance_premium', 
                    'amount_insured', 'deductible_credits', 'annotation',)
    list_filter = ('asset_insured__asset_type__asset_class', 'asset_insured__asset_type', 'asset_insured__actual_place',)
    date_hierarchy = 'end_date'
    
    def get_asset_code(self, obj):
        return obj.asset_insured.asset_code
    get_asset_code.short_description = _(u"Asset code")
    get_asset_code.admin_order_field = 'asset_insured__asset_code'
    
    def get_asset_description(self, obj):
        return obj.asset_insured.description
    get_asset_description.short_description = _(u"Insured asset")
    get_asset_description.admin_order_field = 'asset_insured__description'
    
    def get_asset_place(self, obj):
        return obj.asset_insured.actual_place.name
    get_asset_place.short_description = _(u"Actual asset place")
    get_asset_place.admin_order_field = 'asset_insured__actual_place'
            
admin.site.register(AssetClass, AssetClassAdmin)
admin.site.register(AssetCatalog, AssetCatalogAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(TermModel, TermModelAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(InsurancePolicy, InsurancePolicyAdmin)