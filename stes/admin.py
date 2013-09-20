# -*- coding: utf-8 -*-
#
# File: stes.admin
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
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from stes.models import Bank, Agency, CheckingAccount
 
class BankAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'get_site_url',)
     
    def get_site_url(self, obj):
        return '<a href="%s">%s</a>' % obj.site_url
    get_site_url.short_description = _(u"Site URL")
    get_site_url.allow_tags = True
     
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('bank', 'code', 'name', 'phone', 'fax', 'email', 'contact_name',)
    list_filter = ('bank', 'city',)
     
class CheckingAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'get_bank', 'agency', 'cash_amount',)
    list_filter = ('agency__bank', 'agency',)
    
    def get_bank(self, obj):
        return obj.agency.bank
    get_bank.short_description = _(u"Bank")

 
admin.site.register(Bank, BankAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(CheckingAccount, CheckingAccountAdmin)
