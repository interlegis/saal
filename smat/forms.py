# -*- coding: utf-8 -*-
#
# File: /home/sesostris/workspace/saal/smat/forms.py
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
from django import forms
from smat.models import RequestItem

class RequestItemAdminForm(forms.ModelForm):
    class Meta:
        model = RequestItem
    
    def clean_supply_qty(self):
        if not self.instance._state.adding:
            request_qty = self.instance.request_qty or 0
            supply_qty = self.cleaned_data['supply_qty'] or 0
            material = self.instance.material or None
            avaiable_qty = material.stock_qty or 0
            
            if supply_qty > request_qty:
                raise forms.ValidationError(_(u"Trying to supply more than requested!"))
        
            if supply_qty > avaiable_qty:
                raise forms.ValidationError(_(u"Insufficient stock to supply this item"))

        return self.cleaned_data['supply_qty']
