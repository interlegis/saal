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
from django.contrib import admin
from saal.models import (FederativeUnit, City, LegislativeHouseType,
    LegislativeHouse, OrganizationalUnit, SupplierBase, EmployeeBase)

# Inlines
class OrganizationalUnitInline(admin.TabularInline):
    model = OrganizationalUnit

# ModelAdmins
class CityAdmin(admin.ModelAdmin):
    fieldsets = (
        (_(u'Basic info'), {'fields': ('ibge_code', 'tse_code', 'uf', 'name',)}),
        (_(u'Complementary info'), {'fields': ('is_capital', 'is_hub', 'population', 'creation_date',)}),
        (_(u'Geographic coordinates'), {'fields': ('latitude', 'longitude',)}),
      )
    list_display = ('ibge_code', 'name', 'uf', 'is_capital', 'is_hub', 'population',)
    list_filter = ('is_capital', 'is_hub', 'uf',)
    search_fields = ('name', 'uf__sign', 'uf__name',)
    
class LegislativeHouseAdmin(admin.ModelAdmin):
    fieldsets = (
      (_(u'Basic info'), {'fields': ('name', 'type', 'cnpj', 'observations', 'parliamentarians_qty', 'install_date')}),
      (_(u'Address'), {'fields': ('street', 'neighborhood', 'city', 'zip')}),
      (_(u'Contact'), {'fields': ('phone', 'fax', 'email', 'web_page')})
      )
    raw_id_fields = ('city',)
    list_display = ('name', 'phone', 'fax', 'email', 'web_page')
    list_filter = ('type', 'city__uf',)
    search_fields = ('name', 'city__name',)
    inlines = (OrganizationalUnitInline, )
    
    def has_add_permission(self, request): # For singleton warranty
        return LegislativeHouse.objects.all().count() <= 0         

class SupplierBaseAdmin(admin.ModelAdmin):
    fieldsets = (
      (_(u'Basic info'), {'fields': ('corporate_name', 'invented_name', 'cpf_cnpj', 'state_registry', 'municipal_registry')}),
      (_(u'Address information'), {'fields': ('street', 'neighborhood', 'city', 'zip', 'phone', 'fax', 'email', 'web_page')}),
    )
    raw_id_fields = ('city',)
    list_display = ('cpf_cnpj', 'corporate_name', 'invented_name', 'city', 'phone', 'email',)
    list_filter = ('city__uf', )
    search_fields = ('corporate_name', 'invented_name', 'cpf_cnpj', 'city__name',)

class EmployeeBaseAdmin(admin.ModelAdmin):
#    form = EmployeeFormAdmin
    list_display = ('registration', 'name', 'legislative_house', 'organizational_unit', 'phone', 'cellular_phone', 'email')
    fields = ['name', 'is_disabled', 'phone', 'cellular_phone', 'email', 'registration', 'organizational_unit', 'job_function',
              'auth_user',]
    list_filter = ('legislative_house', 'organizational_unit', 'job_function', 'is_disabled')
    
    def save_model(self, request, obj, form, change):
        if not change and LegislativeHouse.objects.count() > 0:
            obj.legislative_house = LegislativeHouse.objects.all()[0]
        super(EmployeeBaseAdmin, self).save_model(request, obj, form, change)
        
    def has_add_permission(self, request):
        if LegislativeHouse.objects.count() > 0:
            return super(EmployeeBaseAdmin, self).has_add_permission(request)
        else:
            return False
    
    def has_change_permission(self, request, obj=None):
        if LegislativeHouse.objects.count() > 0:
            return super(EmployeeBaseAdmin, self).has_change_permission(request, obj)
        else:
            return False
  
# Register Models
admin.site.register(FederativeUnit)
admin.site.register(City, CityAdmin)
admin.site.register(LegislativeHouseType)
admin.site.register(LegislativeHouse, LegislativeHouseAdmin)
admin.site.register(SupplierBase, SupplierBaseAdmin)
admin.site.register(EmployeeBase, EmployeeBaseAdmin)