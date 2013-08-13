# -*- coding: utf-8 -*-
#
# File: saal.management.commands.create_saal_groups
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
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    def handle(self, *args, **options):
        req_permissions = ['add_request', 'change_request', 'delete_request', 'add_requestitem', 'change_requestitem', 
                           'delete_requestitem', ]
        alm_permissions = ['add_material', 'change_material', 'delete_material', 'add_materialclass', 'change_materialclass', 
                           'delete_materialclass', 'add_purchaseinvoice', 'change_purchaseinvoice', 'delete_purchaseinvoice', 
                           'add_purchaseitem', 'change_purchaseitem', 'delete_purchaseitem', 'can_comply', 'change_requestitem', 
                           'add_reversal', 'change_reversal', 'delete_reversal', 'add_reversalitem', 'change_reversalitem', 
                           'delete_reversalitem', ]

        self.stdout.write('Creating Requisitante group...', ending='')
        requisitante, novo = Group.objects.get_or_create(name='Requisitante')
        if not novo:
            requisitante.permissions.clear()
        for p in Permission.objects.filter(codename__in=req_permissions):
            requisitante.permissions.add(p) 
        requisitante.save()
        self.stdout.write('Done!')
        
        self.stdout.write('Creating Almoxarife group...', ending='')
        almoxarife, novo = Group.objects.get_or_create(name='Almoxarife')
        if not novo:
            almoxarife.permissions.clear()
        for p in Permission.objects.filter(codename__in=alm_permissions):
            almoxarife.permissions.add(p)
        almoxarife.save()
        self.stdout.write('Done!')
        self.stdout.write('Successfully created all SAAL groups')