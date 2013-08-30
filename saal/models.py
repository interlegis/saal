# -*- coding: utf-8 -*-
#
# File: saal.models
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
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models

class FederativeUnit(models.Model):
    """ Represents a state
    """
    ibge_code = models.PositiveIntegerField(
        _(u'IBGE code'),
        primary_key=True,
        unique=True,
        help_text=_(u'State code by IBGE - Brazilian Geographic & Statistical Intitute')
    )
    name = models.CharField(_(u'State name'), max_length=25)
    sign = models.CharField(
        _(u'Sign'),
        max_length=2,
        unique=True,
        help_text=_("Example: <em>MG</em>."),
    )
    population = models.PositiveIntegerField(_(u'population'))

    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Federative Unit')
        verbose_name_plural = _(u'Federative Units')

    def __unicode__(self):
        return self.name

class City(models.Model):
    """ Represents a city
    """
    ibge_code = models.PositiveIntegerField(
        _(u'IBGE code'),
        primary_key=True,
        unique=True,
        help_text=_(u'City code by IBGE - Brazilian Geographic & Statistical Institute')
    )

    # Superior Electoral Court city code
    tse_code = models.PositiveIntegerField(
        _(u'TSE code'),
        unique=True,
        null=True,
        help_text=_(u'City Code by TSE - Superior Electoral Court')
    )
    name = models.CharField(_(u'City name'), max_length=50)
    uf = models.ForeignKey(FederativeUnit, verbose_name=_(u'State'))
    is_capital = models.BooleanField(_(u'Capital'))
    population = models.PositiveIntegerField(_(u'Population'))
    is_hub = models.BooleanField(_(u'Hub'))
    creation_date = models.DateField(_(u'City creation date'), null=True, blank=True)

    # Geographic point
    latitude = models.DecimalField(_(u'Latitude'),
        max_digits=10,
        decimal_places=8,
        null=True,
        blank=True,
        help_text=_(u'Example: <em>-20.464</em>.')
    )
    longitude = models.DecimalField(_(u'Longitude'),
        max_digits=11,
        decimal_places=8,
        null=True,
        blank=True,
        help_text=_(u'Example: <em>-45.426</em>.')
    )

    class Meta:
        ordering = ('name', 'ibge_code')
        verbose_name = _(u'City')
        verbose_name_plural = _(u'Cities')

    def __unicode__(self):
        return u"%s - %s" % (self.name, self.uf)

    def get_google_maps_url(self):
        return "http://maps.google.com.br/maps/mm?ie=UTF8&hl=pt-BR&t=h&ll=%s,%s&spn=1.61886,1.812744&z=9&source=embed" % \
            (self.latitude, self.longitude)

class LegislativeHouseType(models.Model):
    """ Represents types of Legislative Houses
    Generally: City Council, State Legislative and Federal Legislative Houses
    """

    sign = models.CharField(_(u'Sign'), max_length=5)
    name = models.CharField(_(u'Name'), max_length=100)

    class Meta:
        verbose_name = _(u'Legislative house type')
        verbose_name_plural = _(u'Legislative house types')
    
    def __unicode__(self):
        return self.name

class LegislativeHouse(models.Model):
    """ Represents a Legislative House
    """
    name = models.CharField(_(u'Name'),
        max_length=60,
        help_text=_(u'Example: <em>City Council of Springfield</em>.')
    )

    type = models.ForeignKey(LegislativeHouseType, verbose_name=_(u"Type"))
    cnpj = models.CharField(_(u'CNPJ'), max_length=32, blank=True, 
        help_text=_(u'Registration of Legal Entities'))
    observations = models.TextField(_(u'observations'), blank=True)
    parliamentarians_qty = models.PositiveIntegerField(_(u'Quantity of parliamentarians'))

    # Contact informations
    street = models.CharField(_(u'Street'),
        max_length=100,
        help_text=_(u'Avenue, street, lane, alley, square...')
    )
    neighborhood = models.CharField(_(u'Neighborhood'), max_length=100, blank=True)
    city = models.ForeignKey(City, verbose_name=_(u'City'))
    zip = models.CharField(_(u'Zip code'), max_length=10)
    phone = models.CharField(_(u'Phone number'), max_length=32, blank=True)
    fax = models.CharField(_(u'Fax number'), max_length=32, blank=True)
    email = models.EmailField(_(u'E-mail'), max_length=128, blank=True)
    web_page = models.URLField(_(u'Web page'),
        help_text=_(u'Example: <em>http://www.camarapains.mg.gov.br</em>.'),
        blank=True,
    )

    install_date = models.DateField(_(u'Install date'), null=True, blank=True)

    class Meta:
        ordering = ('name',)
        unique_together = ('city', 'type')
        verbose_name = _(u'Legislative house')
        verbose_name_plural = _(u'Legislative houses')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs): # Singleton ensurance
        if self.pk == None: # A new record to be created
            if LegislativeHouse.objects.all().count() > 0: # but only one record already exists
                return # without saving
             
        super(LegislativeHouse, self).save(*args, **kwargs) # save the record.
        
        #Rename all oldgroups, if needed

class OrganizationalUnit(models.Model):
    legislative_house = models.ForeignKey(LegislativeHouse, verbose_name=_(u'Legislative house'))
    account_code = models.CharField(_(u'Account code'), max_length=12, blank=False)
    name = models.CharField(_(u'Name'), max_length=60, blank=False)
    sign = models.CharField(_(u'Sign'), max_length=10, blank=False)
    phone = models.CharField(_(u'Phone number'), max_length=32, blank=True)
    fax = models.CharField(_(u'Fax number'), max_length=32, blank=True)
    email = models.EmailField(_(u'e-mail'), max_length=128, blank=True)
    chief = models.ForeignKey('EmployeeBase', blank=True, null=True, verbose_name=_(u'Chief'))
    parent_ou = models.ForeignKey('self', verbose_name=_(u'Parent Organizational Unit'),
                                  related_name='sub_units', blank=True, null=True)
    
    class Meta:
        ordering = ('legislative_house', 'account_code',)
        unique_together = ('legislative_house', 'account_code',)
        verbose_name = _(u'Organizational unit')
        verbose_name_plural = _(u'Organizational units')
        
    def __unicode__(self):
        return self.name

class SupplierBase(models.Model):
    corporate_name = models.CharField(_(u'Corporate name'), max_length=60)
    invented_name = models.CharField(_(u'Invented name'), max_length=60, blank=True)
    cpf_cnpj = models.CharField(_(u'CPF or CNPJ'), max_length=18)
    state_registry = models.CharField(_(u'State registry'), max_length=30, blank=True)
    municipal_registry = models.CharField(_(u'Municipal registry'), max_length=30, blank=True)
    
    # Contact informations
    street = models.CharField(_(u'Street'),
        max_length=100,
        help_text=_(u'Avenue, street, lane, alley, square...')
    )
    neighborhood = models.CharField(_(u'Neighborhood'), max_length=100, blank=True)
    city = models.ForeignKey(City, verbose_name=_(u'City'))
    zip = models.CharField(_(u'Zip code'), max_length=10)
    phone = models.CharField(_(u'Phone number'), max_length=32, blank=True)
    fax = models.CharField(_(u'Fax number'), max_length=32, blank=True)
    email = models.EmailField(_(u'E-mail'), max_length=128, blank=True)
    web_page = models.URLField(_(u'Web page'),
        help_text=_(u'Example: <em>http://www.camarapains.mg.gov.br</em>.'),
        blank=True,
    )

    class Meta:
        verbose_name = _(u'Supplier')
        verbose_name_plural = _(u'Suppliers')
        
    def __unicode__(self):
        return self.invented_name or self.corporate_name

class EmployeeBase(models.Model):
    ''' base class that represents legislative house employee
    '''
    
#   Personal data 
    name = models.CharField(_(u'Name'), max_length=60)
    is_disabled = models.BooleanField(_(u'Disabled'))
    
#   Contact
    phone = models.CharField(_(u'Phone number'), max_length=32, blank=True)
    cellular_phone = models.CharField(_(u'Cellular phone number'), max_length=32, blank=True)
    email = models.EmailField(_(u'E-mail'), max_length=128, blank=True)
    
#   employment relationship
    registration = models.IntegerField(_(u'Employee registration'))
    legislative_house = models.ForeignKey(LegislativeHouse, verbose_name=_(u'Legislative house'))
    organizational_unit = models.ForeignKey(OrganizationalUnit, verbose_name=_(u'Organizational unit'))
    job_function = models.CharField(_(u'Job function'), max_length=60)
    
    #System access
    auth_user = models.OneToOneField(User, verbose_name=_(u'System user login'), blank=True, null=True)
    
    class Meta:
        ordering = ('legislative_house', 'organizational_unit', 'name',)
        verbose_name = _(u'Employee')
        verbose_name_plural = _(u'Employees')
        
    def __unicode__(self):
        return self.name    