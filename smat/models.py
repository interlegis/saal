# -*- coding: utf-8 -*-
#
# File: models.py
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
from django.db import models
from django.db.models.aggregates import Sum
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from saal.models import EmployeeBase
from saal.models import OrganizationalUnit, SupplierBase

class MaterialClass(models.Model):
    sign = models.CharField(_(u'Sign'), max_length=12)
    description = models.CharField(_(u'Description'), max_length=100)

    class Meta:
        ordering = ('sign',)
        verbose_name = _(u'Material class')
        verbose_name_plural = _(u'Material classes')

    def __unicode__(self):
        return u"%s - %s" % (self.sign, self.description)
    
class Material(models.Model):
    item_code = models.CharField(_(u'Item code'), max_length=12)
    material_class = models.ForeignKey(MaterialClass, verbose_name=_(u'Material class'))
    description = models.CharField(_(u'Description'), max_length=100)
    tecnical_features = models.TextField(_(u'Tecnical features'))
    measure_unit = models.CharField(_(u'Measure unit'), max_length=3)
    stock_min = models.IntegerField(_(u'Minimum stock'))
    stock_max = models.IntegerField(_(u'Maximun stock'))
    supply_point = models.IntegerField(_(u'Supply point'))
    
    class Meta:
        ordering = ('item_code',)
        verbose_name = _(u'Material')
        verbose_name_plural = _(u'Materials')

    def __unicode__(self):
        return u"%s (%s)" % (self.description, self.measure_unit)
    
    @property
    def stock_qty(self):
        return self.materialcluster_set.aggregate(Sum('quantity'))['quantity__sum']
    
    @property
    def stock_cost(self):
        return reduce(lambda x,y: x+y, [c.quantity * c.unit_cost for c in self.materialcluster_set.filter(quantity__gt=0)])

class MaterialCluster(models.Model):
    material = models.ForeignKey(Material, verbose_name=_(u'Material'))
    quantity = models.IntegerField(_(u'Stock quantity'))
    unit_cost = models.DecimalField(_(u'Unit cost'), max_digits=20, decimal_places=2)
    creation_date = models.DateField(_(u'Creation date'), auto_now_add=True)
    last_change = models.DateField(_(u'Last stock change'), auto_now=True)
    
    @property
    def total_cost(self):
        return self.quantity * self.unit_cost

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = _(u'Material cluster')
        verbose_name_plural = _(u'Material clusters')

    def __unicode__(self):
        return _(u"%(quantity)s %(measure_unit)s of %(material)s at cost of %(cost)s") % {'quantity': self.quantity,
		   'measure_unit': self.material.measure_unit, 'material': self.material.description, 'cost': self.unit_cost * self.quantity}

class MaterialMovement(models.Model):
    TYPE_CHOICES = (('E', _(u'Input')), ('S', _(u'Output')))
    
    material_cluster = models.ForeignKey(MaterialCluster, verbose_name=_(u'Material cluster'))
    type = models.CharField(_(u'Type'), max_length=1, choices=TYPE_CHOICES)
    qty_before_mov = models.IntegerField(_(u'Quantity before movement'))
    quantity = models.IntegerField(_(u'Movemented quantity'))
    mov_date = models.DateField(_(u'Movement date'), auto_now_add=True)
    unit_cost = models.DecimalField(_(u'Unit cost'), max_digits=20, decimal_places=2)
    origin = GenericForeignKey()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    
    @property
    def total_cost(self):
        return self.quantity * self.unit_cost

    class Meta:
        ordering = ('-mov_date',)
        verbose_name = _(u'Material movement registry')
        verbose_name_plural = _('Material movements registry')

    def __unicode__(self):
        return _(u"%(type)s %(quantity)s units of %(material)s at %(date)s") % {'type': self.get_type_display(), 
			'quantity': self.quantity, 'material': self.material_cluster.material.description, 'date': self.mov_date}
    
class Request(models.Model):
    STATUS_CHOICES = (
        ('P', _(u'Pending')),
        ('A', _(u'complied')),
      )
    request_unit = models.ForeignKey(OrganizationalUnit, verbose_name=_(u'Requestor unit'))
    requestor = models.ForeignKey(EmployeeBase, verbose_name=_(u'Requestor Employee'), related_name='requests')
    request_date = models.DateField(_(u'Request date'), auto_now_add=True)
    request_status = models.CharField(_(u'Status'), max_length=1, choices=STATUS_CHOICES, default='P', blank=True)
    complied_date = models.DateField(_(u'Complied date'), blank=True, null=True)
    stockman = models.ForeignKey(EmployeeBase, verbose_name=_(u'Stockman'), help_text=_(u'Stockman that comply this request'), 
            related_name='attendances', blank=True, null=True)
    
    @property
    def total_cost(self):
        result = 0
        for item in self.requestitem_set.all():
            result = result + item.total_cost
        return result
    
    class Meta:
        ordering = ('-request_date',)
        verbose_name = _(u'Request')
        verbose_name_plural = _(u'Requests')
        get_latest_by = 'request_date'
        permissions = (('can_comply', _(u'Can comply')),)

    def __unicode__(self):
        return u"%s (%s)" % (self.request_unit, self.request_date)
    
    def save(self, *args, **kwargs):
        self.request_status = 'A' if self.complied_date else 'P'
        super(Request, self).save(*args, **kwargs)

class RequestItem(models.Model):
    request = models.ForeignKey(Request, verbose_name=_(u'Request'))
    material = models.ForeignKey(Material, verbose_name=_(u'Requested material'))
    request_qty = models.IntegerField(_(u'Requested quantity'))
    supply_qty = models.IntegerField(_(u'Supply quantity'), blank=True, null=True)
    movement = GenericRelation('MaterialMovement')

    @property
    def total_cost(self):
        result = 0
        for m in self.movement.all():
            result += m.total_cost
        return result
    
    class Meta:
        verbose_name = _(u'Request item')
        verbose_name_plural = _(u'Request items')

    def __unicode__(self):
        return _(u"%(quantity)s %(measure_unit)s of %(material)s") % {'quantity': self.request_qty, 
			'measure_unit': self.material.measure_unit, 'material': self.material.description}
   
    def save(self, *args, **kwargs):
        if self.request.request_status == 'A':
            # Calcs real qty to debt stock
            todebt = self.supply_qty
            material = self.material
            
            if todebt > material.stock_qty:
                # Partially supply with all avaiable stock
                self.supply_qty = material.stock_qty
                todebt = self.supply_qty
            
            # Debts the MaterialClusters stock quantity
            for cluster in material.materialcluster_set.filter(quantity__gt=0):
                mov = MaterialMovement(material_cluster=cluster, type='S',
                    qty_before_mov=cluster.quantity,unit_cost=cluster.unit_cost,
                    mov_date=date.today(), origin=self)

                if todebt > cluster.quantity:
                    todebt -= cluster.quantity
                    mov.quantity = cluster.quantity
                    cluster.quantity = 0
                else:
                    cluster.quantity -= todebt
                    mov.quantity = todebt
                    todebt = 0
                
                mov.save()
                cluster.save()
                
                if todebt == 0:
                    break
                
        super(RequestItem, self).save(*args, **kwargs)
        
class PurchaseInvoice(models.Model):
    supplier = models.ForeignKey(SupplierBase, verbose_name=_(u'Supplier'))
    number = models.PositiveIntegerField(_(u'Invoice number'))
    serie = models.CharField(_(u'Invoice serie'), max_length=5)
    input_date = models.DateField(_(u'Input date'), auto_now_add=True)
    
    @property
    def total_cost(self):
        result = 0
        for item in self.purchaseitem_set.all():
            result += item.total_cost
        return result
    
    class Meta:
        ordering = ['-input_date']
        verbose_name = _(u'Purchase invoice')
        verbose_name_plural = _(u'Purchase invoices')
        unique_together = ('supplier', 'number', 'serie', )

    def __unicode__(self):
        return _(u"Invoice nr. %(number)s-%(serie)s from %(supplier)s") % {'number': self.number, 'serie': self.serie,
			'supplier': self.supplier.__unicode__()}

class PurchaseItem(models.Model):
    invoice = models.ForeignKey(PurchaseInvoice, verbose_name=_(u'Purchase invoice'))
    material = models.ForeignKey(Material, verbose_name=_(u'Material'))
    material_cluster = models.OneToOneField(MaterialCluster, verbose_name=_(u'Created material cluster'))
    movement = GenericRelation('MaterialMovement')
    quantity = models.PositiveIntegerField(_(u'Quantity'))
    unit_cost = models.DecimalField(_(u'Unit cost'), max_digits=20, decimal_places=2)
    
    @property
    def total_cost(self):
        return self.unit_cost * self.quantity
    
    class Meta:
        verbose_name = _(u'Purchase item')
        verbose_name_plural = _(u'Purchase items')

    def __unicode__(self):
        return _(u"%(quantity)s %(measure_unit)s of %(material)s (invoice nr. %(number)s-%(serie)s:)") % {'quantity': self.quantity,
			'measure_unit': self.material.measure_unit, 'material': self.material.description, 
            		'number': self.invoice.number, 'serie': self.invoice.serie}
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            # Create a new MaterialCluster
            mc = MaterialCluster.objects.create(material=self.material, quantity=self.quantity, unit_cost=self.unit_cost,
                creation_date=self.invoice.input_date, last_change=self.invoice.input_date)
            # Links the MaterialCluster with this PurchaseItem
            self.material_cluster = mc
            # Call the super.save() method
            super(PurchaseItem, self).save(*args, **kwargs)
            # Create a new MaterialMovement
            mm = MaterialMovement.objects.create(material_cluster=mc, type='E', qty_before_mov=0, quantity=self.quantity, 
                mov_date=self.invoice.input_date, unit_cost=self.unit_cost, origin=self)

class Reversal(models.Model):
    TYPE_CHOICES = (('E', _(u'Input')), ('S', _(u'Output')))
    reversal_date = models.DateField(_(u'Reversal date'), auto_now_add=True)
    type = models.CharField(_(u'Type'), max_length=1, choices=TYPE_CHOICES)
    reason = models.TextField(_(u'Reason'))

    class Meta:
        ordering = ['-reversal_date']
        verbose_name = _(u'Reversal')
        verbose_name_plural = _(u'Reversals')

    def __unicode__(self):
        return _(u"%(type)s reversal nr. %(number)s at %(date)s") % {'type': self.get_type_display(), 'number': self.pk,
                                                                     'date': self.reversal_date}

class ReversalItem(models.Model):
    reversal = models.ForeignKey(Reversal, verbose_name=_(u'Reversal'))
    material = models.ForeignKey(Material, verbose_name=_(u'Material'))
    quantity = models.IntegerField(_(u'Movemented quantity'))
    unit_cost = models.DecimalField(_(u'Unit cost'), max_digits=20, decimal_places=2)
    movement = GenericRelation('MaterialMovement') 
    
    class Meta:
        verbose_name = _(u'Reversal item')
        verbose_name_plural = _(u'Reversal items')

    def __unicode__(self):
        return _(u"%(type)s %(quantity)s %(measure_unit)s of %(material)s by reversal Nr. %(number)s") % {'type': self.reversal.get_type_display(),
			'quantity': self.quantity, 'measure_unit': self.material.measure_unit, 'material': self.material.description, 'number':  self.reversal.pk}

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.reversal.type == 'E':
                # Create a new MaterialCluster
                mc = MaterialCluster.objects.create(material=self.material, quantity=self.quantity, unit_cost=self.unit_cost,
                    creation_date=self.reversal.reversal_date, last_change=self.reversal.reversal_date)
                # Call the super.save() method
                super(ReversalItem, self).save(*args, **kwargs)
                # Create a new MaterialMovement
                mm = MaterialMovement.objects.create(material_cluster=mc, type='E', qty_before_mov=0, quantity=self.quantity, 
                    mov_date=self.reversal.reversal_date, unit_cost=self.unit_cost, origin=self)
            elif self.reversal.type == 'S':
                # Calcs real qty to debt stock
                todebt = self.quantity
                material = self.material
            
                if todebt > material.stock_qty:
                # Partially debt with all avaiable stock
                    self.quantity = material.stock_qty
                    todebt = self.quantity
                    
                # Call the super.save() method
                self.unit_cost = 0
                super(ReversalItem, self).save(*args, **kwargs)
            
                # Debts the MaterialClusters stock quantity
                for cluster in material.materialcluster_set.filter(quantity__gt=0):
                    mov = MaterialMovement(material_cluster=cluster, type='S', qty_before_mov=cluster.quantity,unit_cost=cluster.unit_cost,
                        mov_date=self.reversal.reversal_date, origin=self)

                    if todebt > cluster.quantity:
                        todebt -= cluster.quantity
                        mov.quantity = cluster.quantity
                        cluster.quantity = 0
                    else:
                        cluster.quantity -= todebt
                        mov.quantity = todebt
                        todebt = 0
                
                    mov.save()
                    cluster.save()
                
                    if todebt == 0:
                        break
            else:
                raise Exception(_(u"Undefined reversal type. Try 'E' for input or 'S' for output."))
