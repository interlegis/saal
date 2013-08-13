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
from functools import update_wrapper
import ho.pisa as pisa
import cStringIO as StringIO
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_unicode, force_text
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, ListView
from django.contrib import admin
from django.contrib.admin.forms import forms
from django.contrib.admin.options import IncorrectLookupParameters

def fetch_resources(uri, rel):
    path = rel + '/saal' + uri
    return path

class TemplatePdfView(TemplateView):
    pdf_template = None

    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        return [self.pdf_template or 'report/pdf/change_list_pdf.html']

    
    def convert_to_pdf(self, response):
        html = response.content
        pdf = pisa.pisaDocument(src=StringIO.StringIO(html), encoding='utf8', link_callback=fetch_resources)
        if not pdf.err:
            response.content = pdf.dest.getvalue()
            response['Content-Disposition'] = 'attachment; filename=%s.pdf' % self.opts.verbose_name.replace(' ', '_')
        return response
    
    def render_to_response(self, request, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        response = self.response_class(
            request = request,
            template = self.get_template_names(),
            context = context,
            mimetype='application/pdf',
            **response_kwargs
        )
        response.add_post_render_callback(self.convert_to_pdf)
        return response
        
class ModelAdminPdf(admin.ModelAdmin, TemplatePdfView):
    change_list_template = ['report/html/change_list_report.html']
    
    def get(self, request, *args, **kwargs):
        ChangeList = self.get_changelist(request)
        opts = self.model._meta
        app_label = opts.app_label
        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        
        try:
            import sys
            cl = ChangeList(request, self.model, list_display,
                list_display_links, self.list_filter, self.date_hierarchy,
                self.search_fields, self.list_select_related,
                sys.maxint, sys.maxint, self.list_editable,
                self)
            cl.show_all = True
        except IncorrectLookupParameters:
            pass
            # Wacky lookup parameters were given, so redirect to the main
            # changelist page, without parameters, and pass an 'invalid=1'
            # parameter via the query string. If wacky parameters were given
            # and the 'invalid=1' parameter was already in the query string,
            # something is screwed up with the database, so display an error
            # page.
#             if ERROR_FLAG in request.GET.keys():
#                 return SimpleTemplateResponse('admin/invalid_setup.html', {
#                     'title': _('Database error'),
#                 })
#             return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')
        
        cl.formset = None
        
        context = {
            'module_name': force_unicode(opts.verbose_name_plural),
            'title': cl.title,
            'cl': cl,
            'media': self.media,
            'app_label': app_label,
        }
        
        context.update(self.get_context_data(**kwargs))
        
        return self.render_to_response(request, context)       
    
    def get_urls(self):
        from django.conf.urls import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
            url(r'^pdf/$',
                wrap(self.dispatch),
                name='%s_%s_pdf' % info),
        )
        return urlpatterns + super(ModelAdminPdf, self).get_urls()

class TabularListView(forms.Form, ListView):
    _app_label = None
    _title = None
    template_name_pdf = None
    list_fields = None
    groups = []
    totals = []
    page_size = "A4 portrait"
    margin_top = "4cm"
    margin_left = "2cm"
    margin_right = "2cm"
    margin_bottom = "4cm"
    
    def convert_to_pdf(self, response):
        html = response.content
        pdf = pisa.pisaDocument(src=StringIO.StringIO(html), encoding='utf8', link_callback=fetch_resources)
        if not pdf.err:
            response.content = pdf.dest.getvalue()
            response['Content-Disposition'] = 'attachment; filename=%s.pdf' % self.title.replace(' ', '_')
        return response
    
    def form_load_data(self):
        self.data = self.request.GET
        self.is_bound = bool(self.request.GET)
        self.full_clean()
        
    def display_fields(self):
        self.form_load_data()
        return [{'label': self[name].label, 'value': self.cleaned_data[name]} for name in self.cleaned_data]
        
    def filter(self, queryset):
        if self.is_valid():
            try:
                q = {k:v for k,v in self.cleaned_data.items() if v}
                queryset = queryset.filter(**q )
            except:
                return None
        else:
            return None
        
        return queryset
    
    def get_queryset(self):
        queryset = super(TabularListView, self).get_queryset()
        self.form_load_data()
        return self.filter(queryset)

    def get_context_data(self, **kwargs):
        context = super(TabularListView, self).get_context_data(**kwargs)
        self.form_load_data()
        context['form'] = self
        if self.app_label:
            context['app_label'] = self.app_label
        elif hasattr(self.object_list, 'model'):
            opts = self.object_list.model._meta
            context['app_label'] = opts.app_label
        return context
    
    def get(self, request, *args, **kwargs):
        fmt = request.GET.get('fmt', 'html')
        if fmt == 'PDF':
            self.content_type = 'application/pdf'
        response = super(TabularListView, self).get(request, *args, **kwargs)
        if fmt == "PDF":
            response.add_post_render_callback(self.convert_to_pdf)
        return response
    
    def get_template_names(self):
        prefix = 'pdf' if self.request.GET.get('fmt', 'html') == 'PDF' else 'html'
        
        if prefix == 'html' and self.template_name is not None:
            return [self.template_name]

        if prefix == 'pdf' and self.template_name_pdf is not None:
            return [self.template_name_pdf]
        
        try:
            names = super(TabularListView, self).get_template_names()
        except ImproperlyConfigured:
            names = []
            
        if hasattr(self.object_list, 'model'):
            opts = self.object_list.model._meta
            names = ['report/%s/%s/%s/tabular_list.html' %(prefix, opts.app_label, opts.object_name.lower()),
                     'report/%s/%s/tabular_list.html' % (prefix, opts.app_label),
                     'report/%s/tabular_list.html' % prefix,
                    ] + names
        else:
            names = ['report/%s/tabular_list.html' % prefix] + names

        return names

    def get_title(self):
        if self._title is None:
            if hasattr(self.model, '_meta'):
                self._title = _(u'List of %s') % force_text(self.model._meta.verbose_name)
            else:
                self._title = _(u'Tabular list')
        return self._title
    
    def set_title(self, value):
        self._title = value
        
    title = property(get_title, set_title)
    
    def get_app_label(self):
        if self._app_label is None:
            if hasattr(self.model, '_meta'):
                self._app_label = force_text(self.model._meta.app_label)
            else:
                self._app_label = 'unset'
        return self._app_label
    
    def set_app_label(self, value):
        self._app_label = value    
    
    app_label = property(get_app_label, set_app_label)
    
    def table_header(self):
        def get_label(field):
            if 'label' in field:
                return field['label'] 
            field['label'] = field['name'].replace('__',' ').replace('_',' ').title()
            if hasattr(self.object_list, 'model'):
                model = self.object_list.model
                field_names = field['name'].split('__')
                for fn in field_names:
                    try:
                        f = model._meta.get_field(fn)
                        field['label'] = f.verbose_name
                        if hasattr(f, 'related'):
                            model = f.related.parent_model
                    except:
                        return field['label']
            return field['label']
        
        style_property = 'pdf_style' if self.request.GET.get('fmt', 'html') == 'PDF' else 'style'
        result = u""
        for field in self.list_fields:
            label = get_label(field)
            if style_property not in field:
                field[style_property] = ''
            result += u'<th style="%s">%s</th>' % (field[style_property], label)

        return mark_safe(u"<tr>%s</tr>" % result)
    
    def table_footer(self):
        if not self.totals:
            return u""
        style_property = 'pdf_style' if self.request.GET.get('fmt', 'html') == 'PDF' else 'style'
        result = u""
        for field in self.list_fields:
            if style_property not in field:
                field[style_property] = ''
            
            value = u""
            for t in self.totals:
                if t['field'] == field['name']:
                    value = t['label'] % t['value']
                    
            result += u'<th style="%s">%s</th>' % (field[style_property], value)

        return mark_safe(u"<tr>%s</tr>" % result)

    def table_data(self):
        def get_value(obj, f):
            field_names = f['name'].split('__')
            
            for fn in field_names:
                if hasattr(obj, fn):
                    obj = getattr(obj, fn)
                else:
                    try:
                        obj = obj[fn]
                    except:
                        obj = u"??%s??" % fn
            return obj
                
        style_property = 'pdf_style' if self.request.GET.get('fmt', 'html') == 'PDF' else 'style'
        result = u""
        
        # Reset totals
        for t in self.totals:
            t['value'] = None
            
        for g in self.groups:
            g['last_value'] = None
            if 'totals' not in g:
                g['totals'] = []
            for t in g['totals']:
                t['value'] = None 
            
        for obj in self.object_list:
            # Process group breaks
            for g in self.groups:
                value = get_value(obj, {'name': g['group_field']})
                if g['last_value'] is None:
                    g['last_value'] = value
                if g['last_value'] != value:
                    if not g['totals']:
                        result += u'<tr><th colspan="%s">%s %s</th></tr>' % (len(self.list_fields), _(u'End of'), g['last_value'])
                    else:
                        row = u""
                        for f in self.list_fields:
                            if style_property not in f:
                                f[style_property] = ''
                            
                            v = u""
                            for t in g['totals']:
                                if t['field'] == f['name']:
                                    v = t['label'] % {'key': g['last_value'], 'value': t['value']}
                                    t['value'] = None
                                    
                            row += u'<th style="%s">%s</th>' % (f[style_property], v)
                
                        result += u"<tr>%s</tr>" % row
                for t in g['totals']:
                    total_value = get_value(obj, {'name': t['field']})
                    if t['value'] is None:
                        t['value'] = reduce(t['function'], [total_value])
                    else:
                        t['value'] = reduce(t['function'], [total_value], t['value'])
                g['last_value'] = value

            # Calc final totals
            for t in self.totals:
                value = get_value(obj, {'name': t['field']})
                if t['value'] is None:
                    t['value'] = reduce(t['function'], [value])
                else:
                    t['value'] = reduce(t['function'], [value], t['value'])
                
            # Print data
            row = u""
            for f in self.list_fields:
                value = get_value(obj, f)

                if style_property not in f:
                    f[style_property] = ''
                
                row += u'<td style="%s">%s</td>' % (f[style_property], value)
            result += u"<tr>%s</tr>" % row
            
        # Last group calculations
        for g in self.groups:
            if not g['totals']:
                result += u'<tr><th colspan="%s">%s %s</th></tr>' % (len(self.list_fields), _(u'End of'), g['last_value'])
            else:
                row = u""
                for f in self.list_fields:
                    if style_property not in f:
                        f[style_property] = ''
                        
                    v = u""
                    for t in g['totals']:
                        if t['field'] == f['name']:
                            v = t['label'] % {'key': g['last_value'], 'value': t['value']}
                                
                    row += u'<th style="%s">%s</th>' % (f[style_property], v)
            
                result += u"<tr>%s</tr>" % row
            
        return mark_safe(result)