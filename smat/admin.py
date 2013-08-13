# -*- coding: utf-8 -*-
#
# File: admin.py
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
from datetime import date
from django.core.exceptions import PermissionDenied
from django.contrib.admin import helpers
from django.contrib import admin
from saal.reports import ModelAdminPdf
from smat.models import MaterialClass, Material, Request, RequestItem, PurchaseInvoice, PurchaseItem, Reversal, ReversalItem
from smat.filters import StockListFilter
from smat.forms import RequestItemAdminForm
from saal.models import EmployeeBase
    
#Inlines
class RequestItemInline(admin.TabularInline):
    model = RequestItem
    form = RequestItemAdminForm 
    raw_id_fields = ('material',)
    
    def avaiable_stock(self, obj):
        return obj.material.stock_qty or 0
    avaiable_stock.short_description = _(u'Avaiable stock')
  
    def get_fieldsets(self, request, obj=None):
        fieldsets = [(None, {'fields': ('material', 'request_qty') + (('supply_qty', 'avaiable_stock') if 
            request.user.has_perm('smat.can_comply') else ())})]
        return fieldsets
    
    def get_readonly_fields(self, request, obj=None):
        u = request.user
        return ('material', 'request_qty', 'avaiable_stock') if u.has_perm('smat.can_comply') \
            else  ()

    def has_delete_permission(self, request, obj=None):
        return False

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    fields = ('material', 'quantity', 'unit_cost',)
    raw_id_fields = ('material',)

    def get_readonly_fields(self, request, obj=None):
        return ('material', 'quantity', 'unit_cost',) if obj is not None else ()

    def has_delete_permission(self, request, obj=None):
        return super(PurchaseItemInline, self).has_delete_permission(request) if obj is None else False

    def has_add_permission(self, request):
        return super(PurchaseItemInline, self).has_add_permission(request) if request.path.find('add') != -1 else False

class ReversalItemInline(admin.TabularInline):
    model = ReversalItem
    fields = ('material', 'quantity', 'unit_cost',  )
    raw_id_fields = ('material',)

    def get_readonly_fields(self, request, obj=None):
        return ('material', 'quantity', 'unit_cost', ) if obj is not None else ()

    def has_delete_permission(self, request, obj=None):
        return super(ReversalItemInline, self).has_delete_permission(request) if obj is None else False

    def has_add_permission(self, request):
        return super(ReversalItemInline, self).has_add_permission(request) if request.path.find('add') != -1 else False

class ReversalOutputItemInline(ReversalItemInline):
    fields = ('material', 'quantity', )

    def get_readonly_fields(self, request, obj=None):
        return ('material', 'quantity', ) if obj is not None else ()
        
#ModelAdmins
class MaterialClassAdmin(ModelAdminPdf):
    list_display = ('sign', 'description',)
    search_fields = ('sign', 'description',)

class MaterialAdmin(ModelAdminPdf):
    list_display = ('item_code', 'description', 'material_class','stock_qty', 'stock_min', 'stock_max', 'supply_point',)
    list_filter = ('material_class', StockListFilter, )
    list_report = ('item_code', 'description', 'material_class','stock_qty', 'stock_min', 'stock_max', 'supply_point',)
    search_fields = ('description', 'item_code', 'material_class__description', 'material_class__sign')
    
    def has_change_permission(self, request, obj=None):
        if obj == None:
            return True
        return super(MaterialAdmin, self).has_change_permission(request, obj)

class RequestAdmin(admin.ModelAdmin):
    date_hierarchy = 'request_date'
    readonly_fields = ('request_unit', 'requestor', 'request_date', 'stockman', 'complied_date',)
    list_display = ('id', 'request_date', 'request_unit', 'requestor',)
    list_filter = ('request_unit', 'request_date',)
    search_fields = ('request_unit__name', 'requestor__name',)
    inlines = (RequestItemInline,)
    
    def has_change_permission(self, request, obj=None):
        return super(RequestAdmin, self).has_change_permission(request, obj) or request.user.has_perm('smat.can_comply')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = [(_(u'Request'), {'fields': ('request_unit', 'requestor', 'request_date',)})]
        if request.user.has_perm('smat.can_comply'):
            fieldsets = fieldsets + [(_(u'Perform'), {'fields': ('stockman', 'complied_date')})]
        return fieldsets
    
    def  queryset(self, request):
        qs = super(RequestAdmin, self).queryset(request)
        user = request.user
        
        if not user.has_perm('smat.can_comply'):
            qs = qs.filter(requestor__auth_user=user)
            
        return qs.filter(request_status='P')
            
    def add_view(self, request, form_url='', extra_context=None):
        view = super(RequestAdmin, self).add_view(request, form_url, extra_context)
        
        if hasattr(view, 'context_data'):
            user = request.user
            
            if not EmployeeBase.objects.filter(auth_user=user).exists():
                raise PermissionDenied
            
            empl = EmployeeBase.objects.get(auth_user=user)
            obj = Request(request_unit=empl.organizational_unit, requestor=empl, request_date=date.today())
            ModelForm = self.get_form(request, obj)
            form = ModelForm(instance=obj)
            adminForm = helpers.AdminForm(form, self.get_fieldsets(request, obj),
                self.get_prepopulated_fields(request, obj),
                self.get_readonly_fields(request, obj),
                model_admin=self)
            view.context_data['adminform'] = adminForm
        return view
    
    def get_object(self, request, object_id):
        user = request.user
        obj = super(RequestAdmin, self).get_object(request, object_id)
        
        if obj and user.has_perm('smat.can_comply') and EmployeeBase.objects.filter(auth_user=user).exists():
            stockman =  EmployeeBase.objects.get(auth_user=user)
            obj.stockman = stockman
            obj.complied_date = date.today()
            
        return obj
    
    def save_form(self, request, form, change):
        obj = super(RequestAdmin, self).save_form(request, form, change)
        user = request.user
        
        if not EmployeeBase.objects.filter(auth_user=user).exists():
            raise PermissionDenied

        empl = EmployeeBase.objects.get(auth_user=user)
        
        if change:
            if user.has_perm('smat.can_comply'):
                obj.stockman = empl
                obj.complied_date = date.today()
        else:
            obj.request_unit = empl.organizational_unit
            obj.requestor = empl
            obj.request_date=date.today()
            
        return obj

class PurchaseInvoiceAdmin(admin.ModelAdmin):
    date_hierarchy = 'input_date'
    readonly_fields = ('input_date', )
    list_display = ('number', 'serie', 'supplier', 'input_date',)
    list_filter = ('input_date',)
    search_fields = ('supplier__corporate_name', 'supplier__invented_name', 'supplier__cpf_cnpj', 'supplier__city__name', 
        'supplier__city__uf__name', 'supplier__city__uf__sign',)
    inlines = (PurchaseItemInline,)

    def get_readonly_fields(self, request, obj=None):
        if obj is None or obj.pk is None:
            return ('input_date', )
        else:
            return ('supplier', 'number', 'serie', 'input_date',)
        
    def add_view(self, request, form_url='', extra_context=None):
        view = super(PurchaseInvoiceAdmin, self).add_view(request, form_url, extra_context)
        
        if hasattr(view, 'context_data'):
            obj = PurchaseInvoice(input_date=date.today())
            ModelForm = self.get_form(request, obj)
            form = ModelForm(instance=obj)
            adminForm = helpers.AdminForm(form, self.get_fieldsets(request, obj),
                self.get_prepopulated_fields(request, obj),
                self.get_readonly_fields(request, obj),
                model_admin=self)
            view.context_data['adminform'] = adminForm
        return view
    
    def save_model(self, request, obj, form, change):
        if change:
            return
        obj.input_date = date.today()
        super(PurchaseInvoiceAdmin, self).save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False

class ReversalAdmin(admin.ModelAdmin):
    date_hierarchy = 'reversal_date'
    readonly_fields = ('reversal_date', 'type', )
    list_display = ('pk', 'reversal_date', 'type', 'reason', )
    list_filter = ('reversal_date', 'type', )
    inlines = (ReversalItemInline, )
    
    def get_readonly_fields(self, request, obj=None):
        if obj is None or obj.pk is None:
            return ('reversal_date', 'type', )
        else:
            return ('reason', 'reversal_date', 'type', )

    def get_inline_instances(self, request, obj):
        #TODO: Verificar tipo quando estiver alterando
        if request.GET.get('_input', '1') == '0':
            self.inlines = (ReversalOutputItemInline, )
        else:
            self.inlines = (ReversalItemInline, )
        
        return super(ReversalAdmin, self).get_inline_instances(request)
 
    def add_view(self, request, form_url='', extra_context=None):
        view = super(ReversalAdmin, self).add_view(request, form_url, extra_context)
        is_input = request.GET.get('_input', '1') == '1'
        if hasattr(view, 'context_data'):
            obj = Reversal(reversal_date=date.today())
            obj.type = 'E' if is_input else 'S'
            ModelForm = self.get_form(request, obj)
            form = ModelForm(instance=obj)
            adminForm = helpers.AdminForm(form, self.get_fieldsets(request, obj),
                self.get_prepopulated_fields(request, obj),
                self.get_readonly_fields(request, obj),
                model_admin=self)
            view.context_data['adminform'] = adminForm
        return view
    
    def save_model(self, request, obj, form, change):
        if change:
            return
        obj.input_date = date.today()
        obj.type = 'E' if request.GET.get('_input', '1') == '1' else 'S'
        super(ReversalAdmin, self).save_model(request, obj, form, change)
        
    def has_delete_permission(self, request, obj=None):
        return False
    
# Register Models
admin.site.register(Material, MaterialAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(MaterialClass, MaterialClassAdmin)
admin.site.register(PurchaseInvoice, PurchaseInvoiceAdmin)
admin.site.register(Reversal, ReversalAdmin)