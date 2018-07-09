from django.forms.models import modelform_factory
from django.forms.widgets import Input
from django.forms import ModelChoiceField, PasswordInput
from django_addanother.contrib.select2 import Select2AddAnother, Select2MultipleAddAnother
from dataclasses import dataclass
from typing import Dict, Tuple
from datetime import datetime

@dataclass
class Widget:
    html: str
    css: Dict[str, Tuple[str]]
    js: Tuple[str]

WIDGETS_AVAILABLE = {
    'DateField': Widget('widgets/date.html',
                {'all': ('external/tempusdominus-bootstrap-4.min.css',)},
                ('external/jquery-3.3.1.min.js',
                  'external/moment-with-locales.min.js',
                  'external/tempusdominus-bootstrap-4.min.js',
                  'widgets/date.js')),
    'DateTimeField': Widget('widgets/datetime.html',
                    {'all': ('external/tempusdominus-bootstrap-4.min.css',)},
                    ('external/jquery-3.3.1.min.js',
                          'external/moment-with-locales.min.js',
                          'external/tempusdominus-bootstrap-4.min.js',
                          'widgets/datetime.js')),
    'ForeignKey': '',
    'ManyToManyField': ''}

CONVERT = {'today': datetime.now().strftime('%Y-%m-%d'),
           'locale': 'fr'}

def get_attrs(attrs):
    ''' Convert attr from models to widgets '''
    attrs = dict(attrs)
    for k, v in attrs.items():
        attrs[k] = CONVERT[v]
    return attrs

def get_widgets(f):
    ftype = f.get_internal_type()
    if ftype == 'ForeignKey':
        model_name = f.related_model._meta.model_name.capitalize()
        w = Select2AddAnother(f'/{model_name}/create')
        w.attrs['data-placeholder'] = f'[{model_name}]'
        return w
    elif ftype == 'ManyToManyField':
        model_name = f.related_model._meta.model_name.capitalize()
        w = Select2MultipleAddAnother(f'/{model_name}/create')
        w.attrs['data-placeholder'] = f'[{model_name}]'
        return w

    w = WIDGETS_AVAILABLE[ftype]
    fattrs = get_attrs(f.choices)
    class GenericWidget(Input):
        template_name = w.html
        def get_context(self, name, value, attrs):
            attrs.update(fattrs)
            context = super(GenericWidget, self).get_context(f.name, value, attrs)
            if not f.blank:
                context['widget']['attrs']['required'] = 'required'
            return context
        class Media:
            css = w.css
            js = w.js
    return GenericWidget

class ModelFormWidgetMixin(object):
    def get_form_class(self):
        f = modelform_factory(
            self.model, exclude=self.exclude, widgets=self.widgets)
        f.field_order= ('username', 'password', 'last_name', 'first_name', 'email')
        return f
