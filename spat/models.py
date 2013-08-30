# -*- coding: utf-8 -*-
#
# File: spat.models
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
from django.db import models
from django.db.models import F
from django.db.transaction import commit_on_success
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from tinymce.models import HTMLField
from saal.models import SupplierBase, OrganizationalUnit, EmployeeBase

class TermModel(models.Model):
    TERM_TYPE_CHOICES = (
        ('T', _(u"Transfer term")),
        ('W', _(u"Writedown term")),
        ('C', _(u"Change term")),
        ('D', _(u"Depreciation term")),)
# Translators: These terms are used in macrosubstitution in Term Model redaction. DO NOT translate the {{ }} enclosed keys!!!!
    TERM_TEXT_HELP = _(u"""<strong>The folowing terms can be used for macrosubstitution in term text body:</strong><br/>
<ul>
    <li>{{ asset_code }} : The asset account code</li>
    <li>{{ asset_type }} : The asset catalog type</li>
    <li>{{ asset_description }} : The asset description</li>
    <li>{{ registry_date }} : The date of movement registry</li>
    <li>{{ registry_annotation }} : The movement registry additional annotations</li>
    <li>{{ transfer_from_unit }} : Organizational Unit transfer origin - for transfer registries only</li>
    <li>{{ transfer_to_unit }} : Organizational Unit transfer target - for transfer registries only</li>
    <li>{{ transfer_from_chief }} : The Organizational Unit transferor chief name - for transfer registries only</li>
    <li>{{ transfer_to_chief }} : The Organizational Unit receiver chief name - for transfer registries only</li>
    <li>{{ writedown_cause }} : The cause of writedown asset - for writedown registries only</li>
    <li>{{ asset_old_value }} : The old asset value - for depreciation/change registries only</li>
    <li>{{ asset_old_description }} : The old asset description - for change registries only</li>
    <li>{{ depreciation_value }} : The value of depreciation - for depreciation registries only</li>
    <li>{{ asset_new_value }} : The new asset value - for depreciation/change registries only</li>
    <li>{{ asset_new_description }} : The new asset description - for change registries only</li>
</ul>""")
    term_type = models.CharField(_(u"Model type"), max_length=1, choices=TERM_TYPE_CHOICES)
    model_name = models.CharField(_(u"Model name"), max_length=100)
    is_active = models.BooleanField(_(u"Is active?"))
    term_text = HTMLField(_(u"Text term"), help_text=TERM_TEXT_HELP)
         
    class Meta:
        ordering = ('term_type', 'is_active', 'model_name',)
        verbose_name, verbose_name_plural = _(u'Term model'), _(u'Term models')
 
    def __unicode__(self):
        return u"%s: %s" % (self.get_term_type_display(), self.model_name)

class AssetClass(models.Model):
    sign = models.CharField(_(u'Sign'), max_length=12)
    description = models.CharField(_(u'Description'), max_length=100)

    class Meta:
        ordering = ('sign',)
        verbose_name, verbose_name_plural = _(u'Asset class'), _(u'Asset classes')

    def __unicode__(self):
        return u"%s - %s" % (self.sign, self.description)

class AssetCatalog(models.Model):
    item_code = models.CharField(_(u'Item code'), max_length=12)
    asset_class = models.ForeignKey(AssetClass, verbose_name=_(u'Asset class'))
    description = models.CharField(_(u'Description'), max_length=100)
    tecnical_features = models.TextField(_(u'Tecnical features'))

    class Meta:
        ordering = ('asset_class', 'item_code', 'description',)
        verbose_name, verbose_name_plural = _(u'Asset catalog'), _(u'Assets catalog')

    def __unicode__(self):
        return u"%s - %s" % (self.item_code, self.description)

class Asset(models.Model):
    ACQUISITION_TYPE_CHOICES = (
        (1, _(u"Contract")),
        (2, _(u"Expropriation")),
        (3, _(u"Prescription")),
        (4, _(u"Confiscation")),
        (5, _(u"Accession")),
        (6, _(u"acquisition causa mortis")),
        (7, _(u"Public sale")),
        (8, _(u"Adjudication")),
        (9, _(u"allotment")),
        (10, _(u"Reversion")),
        (11, _(u"Abandonment")),)
    STATUS_CHOICES = (
        ('U', _(u'In use')),
        ('D', _(u'Write down')),
    )
    asset_code = models.CharField(_(u'Asset record code'), max_length=12, unique=True)
    asset_type = models.ForeignKey(AssetCatalog, verbose_name=_(u"Asset type"))
    description = models.TextField(_(u'Description'))
    actual_place = models.ForeignKey(OrganizationalUnit, verbose_name=_(u"Actual place"))
    classification_code = models.CharField(_(u"Classification code"), max_length=12)
    acquisition_type =  models.PositiveSmallIntegerField(_(u"Acquisition type"), choices=ACQUISITION_TYPE_CHOICES)
    acquisition_doc_type = models.CharField(_(u"Acquisition document type"), max_length=100)
    acquisition_doc_num = models.CharField(_(u"Acquisition document number"), max_length=100)
    supplier = models.ForeignKey(SupplierBase, verbose_name=_(u"Supplier"))
    acquisition_date = models.DateField(_(u"Acquisition date"))
    acquisition_value = models.DecimalField(_(u"Acquisition value"), max_digits=20, decimal_places=2)
    actual_value = models.DecimalField(_(u"Actual value"), max_digits=20, decimal_places=2,)
    status = models.CharField(_(u"Actual state"), max_length=1, choices=STATUS_CHOICES, default='U', editable=False)
    
    class Meta:
        ordering = ('actual_place', 'status', 'asset_type',)
        verbose_name, verbose_name_plural = _(u'Asset'), _(u'Assets')

    def __unicode__(self):
        return _(u"%(asset_code)s in %(actual_place)s" % {'asset_code': self.asset_code, 'actual_place': self.actual_place})

class AssetMovement(models.Model):
    asset = models.ForeignKey(Asset, verbose_name=_(u"Asset"))
    mov_date = models.DateTimeField(_(u"Movement date"), auto_now_add=True, editable=False)
    origin = GenericForeignKey()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    
    @property
    def annotation(self):
        return self.origin.annotation
    
    class Meta:
        ordering = ('-mov_date',)
        verbose_name, verbose_name_plural = _(u"Asset movement"), _(u"Asset movements")
        
    def __unicode__(self):
        return _(u"Movement id: %s" % self.pk)

class AbstractRegistry(models.Model):
    asset = models.ForeignKey(Asset, verbose_name=_(u"Asset"))
    registry_date = models.DateTimeField(_(u"Registry date"), auto_now_add=True, editable=False)
    annotation = models.TextField(_(u"Additional annotation"))
    related_movement = GenericRelation('AssetMovement')

    class Meta:
        abstract = True
        ordering = ('asset', '-registry_date',)
    
    def pre_save(self, asset):
        """
        Hook for doing any pre save model changes has been
        called before any data saves
        """
        pass

    def post_save(self, asset):
        """
        Hook for doing any post save model actions has been
        called afetr model saves and before AssetMovement creation
        """
        pass

    @commit_on_success
    def save(self, *args, **kwargs):
        asset = self.asset
        self.pre_save(asset)
        super(AbstractRegistry, self).save(*args, **kwargs)
        self.post_save(asset)
        if not self.related_movement.exists():
            mov = AssetMovement(asset=asset, mov_date=self.registry_date, origin=self)
        else:
            mov = self.related_movement.get()
            mov.asset = asset
            mov.mov_date = self.registry_date
        mov.save()

class TransferRegistry(AbstractRegistry):
    term_model = models.ForeignKey(TermModel, verbose_name=_(u"Term model"), limit_choices_to={'is_active': True, 'term_type': 'T'})
    from_unit = models.ForeignKey(OrganizationalUnit, verbose_name=_(u"From unit"), related_name='out_transfers')
    from_chief = models.ForeignKey(EmployeeBase, verbose_name=_(u"From chief"), related_name='out_transfers')
    to_unit = models.ForeignKey(OrganizationalUnit, verbose_name=_(u"To unit"), related_name='in_transfers')
    to_chief = models.ForeignKey(EmployeeBase, verbose_name=_(u"To chief"), related_name='in_transfers')
    
    class Meta(AbstractRegistry.Meta):
        verbose_name, verbose_name_plural = _(u"Asset transfer registry"), _(u"Asset transfer registries")
        
    def __unicode__(self):
        return _(u"Asset %(asset)s transfered from %(from_unit)s to %(to_unit)s at %(transfer_date)s." % 
                 {'asset': self.asset.asset_code, 'from_unit': self.from_unit, 'to_unit': self.to_unit, 
                  'transfer_date': self.registry_date})

    def pre_save(self, asset):        
        self.from_unit = asset.actual_place
        self.from_chief = asset.actual_place.chief
        self.to_chief = self.to_unit.chief
        
    def post_save(self, asset):
        asset.actual_place = self.to_unit
        asset.save()

class WriteDownRegistry(AbstractRegistry):
    DOWN_CAUSE_CHOICES = (
        (1, _(u'Disposal')),
        (2, _(u'Donation')),
        (3, _(u'Exchange')),
        (4, _(u'Dation in payment')),
        (5, _(u'Domain concession')),
        (6, _(u'Legitimizing possession')),
        (7, _(u'Investiture')),
        (8, _(u'Incorporation or inversion')),
        (9, _(u'Retrocession')),
        (10, _(u'theft')),
        (11, _(u'disuse')),
        (12, _(u'Other')))
    term_model = models.ForeignKey(TermModel, verbose_name=_(u"Term model"), limit_choices_to={'is_active': True, 'term_type': 'W'})
    down_cause = models.PositiveSmallIntegerField(_(u"Writedown cause"), choices=DOWN_CAUSE_CHOICES)
    
    class Meta(AbstractRegistry.Meta):
        verbose_name, verbose_name_plural = _(u"Asset writedown registry"), _(u"Asset writedown registries")
        
    def __unicode__(self):
        return _(u"Asset %(asset)s writed down in %(down_date)s. by %(down_cause)s" % 
                 {'asset': self.asset.asset_code, 'down_date': self.registry_date, 'down_cause': self.get_down_cause_display(),}) 

    def post_save(self, asset):
        asset.status = 'D'
        asset.save()

class DepreciationRegistry(AbstractRegistry):
    term_model = models.ForeignKey(TermModel, verbose_name=_(u"Term model"), limit_choices_to={'is_active': True, 'term_type': 'D'})
    old_value = models.DecimalField(_(u"Old value"), max_digits=20, decimal_places=2)
    depreciation_value = models.DecimalField(_(u"Depreciation value"), max_digits=20, decimal_places=2)
    new_value = models.DecimalField(_(u"New value"), max_digits=20, decimal_places=2)

    def __unicode__(self):
        return _(u"Asset %(asset)s depreciated down in %(depreciation_date)s. by U$ %(depreciation_value)s" % 
                 {'asset': self.asset.asset_code, 'depreciation_date': self.registry_date,
                  'depreciation_value': self.depreciation_value,})

    def pre_save(self, asset):
        self.old_value = asset.actual_value
        self.new_value = asset.actual_value - self.depreciation_value
        
    def post_save(self, asset):
        asset.actual_value = F('actual_value') - self.depreciation_value
        asset.save()
        
class ChangeRegistry(AbstractRegistry):
    term_model = models.ForeignKey(TermModel, verbose_name=_(u"Term model"), limit_choices_to={'is_active': True, 'term_type': 'C'})
    old_value = models.DecimalField(_(u"Old value"), max_digits=20, decimal_places=2)
    old_description = models.TextField(_(u'Old description')) 
    new_value = models.DecimalField(_(u"New value"), max_digits=20, decimal_places=2)
    new_description = models.TextField(_(u'New description'))

    def __unicode__(self):
        return _(u"Asset %(asset)s changed in %(change_date)s. from '%(old_description)s' and 'U$ %(old_value)s' to '%(new_description)s and 'U$ %(new_value)s'" % 
                 {'asset': self.asset.asset_code, 'change_date': self.registry_date, 'old_description': self.old_description,
                  'old_value': self.old_value, 'new_description': self.new_description, 'new_value': self.new_value})

    def pre_save(self, asset):
        self.old_value = asset.actual_value
        self.old_description = asset.description
        
    def post_save(self, asset):
        asset.actual_value = self.new_value
        asset.description = self.new_description
        asset.save()

class Inventory(models.Model):
    year_month = models.CharField(_(u"Year/month"), max_length=6, primary_key=True)
    hidden_year_month_fstday = models.DateField()
    generation_date = models.DateTimeField(_(u"Generation date"), auto_now=True)
    total_value = models.DecimalField(_(u"Total value"), max_digits=20, decimal_places=2)
    
    class Meta:
        ordering = ('-year_month',)
        verbose_name, verbose_name_plural = _(u"Monthly inventory"), _(u"Monthly inventories")
        
    def __unicode__(self):
        return _(u"Inventory for %(year_month)s generated at %(generation_date)s: U$ %(total_value)s" % 
                 {'year_month': self.year_month, 'generation_date': self.generation_date, 'total_value': self.total_value,})
    
    @commit_on_success
    def save(self, *args, **kwargs):
        is_new = not Inventory.objects.filter(pk=self.pk).exists()
        if is_new:
            self.total_value = 0
            self.hidden_year_month_fstday = self.year_month[:4] + '-' + self.year_month[4:] + '-01' 
        super(Inventory, self).save(*args, **kwargs)
        if is_new:
            for asset in Asset.objects.filter(status='U'):
                det = InventoryDetail(inventory=self, asset=asset, unit=asset.actual_place, asset_description=asset.description,
                                      asset_value=asset.actual_value)
                det.save()
                self.total_value += det.asset_value
            self.save()

class InventoryDetail(models.Model):
    inventory = models.ForeignKey(Inventory)
    asset = models.ForeignKey(Asset)
    unit = models.ForeignKey(OrganizationalUnit)
    asset_description = models.TextField(_(u'Description'))
    asset_value = models.DecimalField(_(u"Actual value"), max_digits=20, decimal_places=2,)

    class Meta:
        ordering = ('inventory', 'unit', 'asset')
        unique_together = ('inventory', 'asset')
        verbose_name, verbose_name_plural = _(u"Monthly inventory detail"), _(u"Monthly inventory details")
        
    def __unicode__(self):
        return _(u"Asset %(asset_code)s guarded by %(unit)s in %(year_month)s with value U$ %(asset_value)s" % 
                 {'asset_code': self.asset.asset_code, 'unit': self.unit.name,'year_month': self.inventory.year_month,
                  'asset_value': self.asset_value, })
        
class InsurancePolicy(models.Model):
    policy_id = models.CharField(_(u"Policy identifier"), max_length=12)
    asset_insured = models.ForeignKey(Asset, verbose_name=_(u"Asset"))
    start_date = models.DateField(_(u"Validity start date"))
    end_date = models.DateField(_(u"Expiration date"))
    insurance_premium = models.DecimalField(_(u"Insurance premium"), max_digits=20, decimal_places=2)
    amount_insured = models.DecimalField(_(u"Amount insured"), max_digits=20, decimal_places=2)
    deductible_credits = models.DecimalField(_(u"Deductible credits"), max_digits=20, decimal_places=2)
    annotation = models.TextField(_(u"Additional annotation"))
    
    class Meta:
        ordering = ('-end_date', )
        verbose_name, verbose_name_plural = _(u"Insurance policy"), _(u"Insurance policies")
        
    def __unicode__(self):
        return _("Policy %(policy_id)s for asset %(asset_code)s." % {'policy_id': self.policy_id, 
                    'asset_code': self.asset_insured.asset_code, })    