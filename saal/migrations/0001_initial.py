# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FederativeUnit'
        db.create_table(u'saal_federativeunit', (
            ('ibge_code', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('sign', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
            ('population', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'saal', ['FederativeUnit'])

        # Adding model 'City'
        db.create_table(u'saal_city', (
            ('ibge_code', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, primary_key=True)),
            ('tse_code', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('uf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['saal.FederativeUnit'])),
            ('is_capital', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('population', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_hub', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=8, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'saal', ['City'])

        # Adding model 'LegislativeHouseType'
        db.create_table(u'saal_legislativehousetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sign', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'saal', ['LegislativeHouseType'])

        # Adding model 'LegislativeHouse'
        db.create_table(u'saal_legislativehouse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['saal.LegislativeHouseType'])),
            ('cnpj', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('observations', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parliamentarians_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('neighborhood', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['saal.City'])),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=128, blank=True)),
            ('web_page', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('install_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'saal', ['LegislativeHouse'])

        # Adding unique constraint on 'LegislativeHouse', fields ['city', 'type']
        db.create_unique(u'saal_legislativehouse', ['city_id', 'type_id'])

        # Adding model 'OrganizationalUnit'
        db.create_table(u'saal_organizationalunit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('legislative_house', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['saal.LegislativeHouse'])),
            ('account_code', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('sign', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=128, blank=True)),
            ('parent_ou', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sub_units', null=True, to=orm['saal.OrganizationalUnit'])),
        ))
        db.send_create_signal(u'saal', ['OrganizationalUnit'])

        # Adding unique constraint on 'OrganizationalUnit', fields ['legislative_house', 'account_code']
        db.create_unique(u'saal_organizationalunit', ['legislative_house_id', 'account_code'])

        # Adding model 'SupplierBase'
        db.create_table(u'saal_supplierbase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('corporate_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('invented_name', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('cpf_cnpj', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('state_registry', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('municipal_registry', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('neighborhood', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['saal.City'])),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=128, blank=True)),
            ('web_page', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'saal', ['SupplierBase'])

        # Adding model 'EmployeeBase'
        db.create_table(u'saal_employeebase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('is_disabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('cellular_phone', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=128, blank=True)),
            ('registration', self.gf('django.db.models.fields.IntegerField')()),
            ('legislative_house', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['saal.LegislativeHouse'])),
            ('organizational_unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['saal.OrganizationalUnit'])),
            ('job_function', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('auth_user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'saal', ['EmployeeBase'])


    def backwards(self, orm):
        # Removing unique constraint on 'OrganizationalUnit', fields ['legislative_house', 'account_code']
        db.delete_unique(u'saal_organizationalunit', ['legislative_house_id', 'account_code'])

        # Removing unique constraint on 'LegislativeHouse', fields ['city', 'type']
        db.delete_unique(u'saal_legislativehouse', ['city_id', 'type_id'])

        # Deleting model 'FederativeUnit'
        db.delete_table(u'saal_federativeunit')

        # Deleting model 'City'
        db.delete_table(u'saal_city')

        # Deleting model 'LegislativeHouseType'
        db.delete_table(u'saal_legislativehousetype')

        # Deleting model 'LegislativeHouse'
        db.delete_table(u'saal_legislativehouse')

        # Deleting model 'OrganizationalUnit'
        db.delete_table(u'saal_organizationalunit')

        # Deleting model 'SupplierBase'
        db.delete_table(u'saal_supplierbase')

        # Deleting model 'EmployeeBase'
        db.delete_table(u'saal_employeebase')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'saal.city': {
            'Meta': {'ordering': "('name', 'ibge_code')", 'object_name': 'City'},
            'creation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'ibge_code': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_capital': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_hub': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '8', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'population': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tse_code': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True'}),
            'uf': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['saal.FederativeUnit']"})
        },
        u'saal.employeebase': {
            'Meta': {'ordering': "('legislative_house', 'organizational_unit', 'name')", 'object_name': 'EmployeeBase'},
            'auth_user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'cellular_phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_function': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'legislative_house': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['saal.LegislativeHouse']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'organizational_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['saal.OrganizationalUnit']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'registration': ('django.db.models.fields.IntegerField', [], {})
        },
        u'saal.federativeunit': {
            'Meta': {'ordering': "('name',)", 'object_name': 'FederativeUnit'},
            'ibge_code': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'population': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sign': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'})
        },
        u'saal.legislativehouse': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('city', 'type'),)", 'object_name': 'LegislativeHouse'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['saal.City']"}),
            'cnpj': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'install_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'observations': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parliamentarians_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['saal.LegislativeHouseType']"}),
            'web_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'saal.legislativehousetype': {
            'Meta': {'object_name': 'LegislativeHouseType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'saal.organizationalunit': {
            'Meta': {'ordering': "('legislative_house', 'account_code')", 'unique_together': "(('legislative_house', 'account_code'),)", 'object_name': 'OrganizationalUnit'},
            'account_code': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legislative_house': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['saal.LegislativeHouse']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'parent_ou': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sub_units'", 'null': 'True', 'to': u"orm['saal.OrganizationalUnit']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'saal.supplierbase': {
            'Meta': {'object_name': 'SupplierBase'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['saal.City']"}),
            'corporate_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'cpf_cnpj': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invented_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'municipal_registry': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'state_registry': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'web_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['saal']