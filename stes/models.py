# -*- coding: utf-8 -*-
#
# File: 
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
from django.utils.translation import gettext as _

from django.db import models
from saal.models import City , EmployeeBase
 
class Bank(models.Model):
    code = models.PositiveIntegerField(_(u"Bank code"), primary_key=True)
    name = models.CharField(_(u"Bank name"), max_length=100)
    site_url = models.URLField(_(u"Site URL"))
 
    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Bank')
        verbose_name_plural = _(u'Banks')
 
    def __unicode__(self):
        return "%s - %s" % [self.code, self.name]
 
class Agency(models.Model):
    bank = models.ForeignKey(Bank, verbose_name=_(u"Bank"))
    code = models.CharField(_(u"Agency code"), max_length=20)
    name = models.CharField(_(u"Agency name"), max_length=100)
    street = models.CharField(_(u'Street'), max_length=100, help_text=_(u'Avenue, street, lane, alley, square...'))
    neighborhood = models.CharField(_(u'Neighborhood'), max_length=100, blank=True)
    city = models.ForeignKey(City, verbose_name=_(u'City'))
    zip = models.CharField(_(u'Zip code'), max_length=10)
    phone = models.CharField(_(u'Phone number'), max_length=32, blank=True)
    fax = models.CharField(_(u'Fax number'), max_length=32, blank=True)
    email = models.EmailField(_(u'E-mail'), max_length=128, blank=True)
    contact_name = models.CharField(_(u"Agency contact name"), max_length=100)
     
    class Meta:
        ordering = ('name',)
        unique_together = ('bank', 'code')
        verbose_name = _(u'Bancary agency')
        verbose_name_plural = _(u'Bancary agencies')
 
    def __unicode__(self):
        return "%s - %s" % [self.name, self.bank.name]
 
class CheckingAccount(models.Model):
    agency = models.ForeignKey(Agency, verbose_name=_(u"Agency"))
    account_number = models.PositiveIntegerField(_(u"Account number"))
    open_date = models.DateField(_(u"Opening account date"))
    close_date = models.DateField(_(u"Closing account date"))
    cash_amount = models.DecimalField(_(u"Cash amount"), max_digits=20, decimal_places=2)
    manager = models.ForeignKey(EmployeeBase, verbose_name=_(u"Employee manager"), 
        help_text=_(u"Employee that is registered under the bank as account manager."))
     
    class Meta:
        ordering = ('account_number',)
        unique_together = ('agency', 'account_number')
        verbose_name = _(u'Checking account')
        verbose_name_plural = _(u'Checking accounts')
 
    def __unicode__(self):
        return "%s: %s - %s" % [self.account_number, self.agency.bank.name, self.agency.name,]