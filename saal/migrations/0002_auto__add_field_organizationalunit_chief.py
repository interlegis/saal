# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'OrganizationalUnit.chief'
        db.add_column(u'saal_organizationalunit', 'chief',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['saal.EmployeeBase'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'OrganizationalUnit.chief'
        db.delete_column(u'saal_organizationalunit', 'chief_id')


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
            'chief': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['saal.EmployeeBase']", 'null': 'True', 'blank': 'True'}),
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