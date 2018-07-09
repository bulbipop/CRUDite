import django_tables2 as tables
from django.apps import apps
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import select_template
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_addanother.views import CreatePopupMixin
from django_filters import FilterSet
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from . import forms
from . import models as m

EXCLUDE = ['id', 'user_permissions', 'is_staff', 'is_active', 'is_superuser',
           'last_login', 'date_joined']
FOREIGN = ('OneToOneField', 'ForeignKey', 'ManyToManyField')


def generate_widgets(model):
    widgets = {'password': forms.PasswordInput()}
    for f in model._meta.get_fields():
        if f.get_internal_type() in forms.WIDGETS_AVAILABLE:
            widgets[f.name] = forms.get_widgets(f)
    return widgets


def generic_template(request, template):
    class Generic(LoginRequiredMixin, TemplateView):
        template_name = f'{template}.html'
    return Generic.as_view()(request)


def list_view(request, model_name, objects=None, seq_order=None, not_in=None):
    mod = apps.get_model(f'{__package__}.{model_name}')
    objects = objects or mod.objects.all()
    order = request.GET['sort'] if 'sort' in request.GET else ''
    if seq_order is None:
        seq_order = ['actions']
        not_in = not_in or []
        for f in mod._meta.get_fields():
            if f.get_internal_type() not in FOREIGN:
                if f.name not in EXCLUDE and f.name not in not_in:
                    seq_order.append(f.name)
                    continue
            not_in.append(f.name)

    class GenericFilter(FilterSet):
        class Meta:
            model = mod
            fields = [col for col in seq_order if col != 'actions']

    class Generic(tables.Table):
        actions = tables.Column('Actions', accessor='id', orderable=False)

        def render_actions(self, record):
            return format_html('''
                    <a href="./update/{0}" title="{1}">📝</a>
                    <a href="./{0}" title="{2}">🔍</a>
                    <a href="./delete/{0}" class="delete" title="{3}">🗑</a>
                    ''', record.pk, 'Éditer', 'Détails', 'Supprimer')

        class Meta:
            model = mod
            row_attrs = {
                'data-id': lambda record: record.pk
            }
            exclude = not_in
            sequence = seq_order
            template = 'table.html'
            order_by = order

    class GenericFilteredListView(LoginRequiredMixin,
                                  PermissionRequiredMixin,
                                  SingleTableMixin,
                                  FilterView):
        permission_required = f'{model_name}.view_{model_name}'
        table_class = Generic
        filterset_class = GenericFilter
        model = mod
        template_name = 'list.html'
    return GenericFilteredListView.as_view()(request)


def details_view(request, model_name, pk):
    class GenericDetail(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        DetailView):
        permission_required = f'{model_name}.view_{model_name}'
        model = apps.get_model(f'{__package__}.{model_name}')
        template_name = select_template(
            [f'{model_name}_details.html', 'details.html']).template.name

        def get_object(self, obj=model.objects.get(id=pk)):
            return obj

        def field_names(self, obj=[f.name for f in model._meta.get_fields()]):
            return obj
    return GenericDetail.as_view()(request)


def create(request, model_name):
    class GenericCreate(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        forms.ModelFormWidgetMixin,
                        CreatePopupMixin,
                        CreateView):
        permission_required = f'{model_name}.create_{model_name}'
        model = apps.get_model(f'{__package__}.{model_name}')
        template_name = select_template(
            [f'{model_name}_create.html', 'create.html']).template.name
        success_url = f'/{model_name}'
        exclude = EXCLUDE
        widgets = generate_widgets(model)
    return GenericCreate.as_view()(request)


def update(request, model_name, pk):
    class GenericUpdate(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        forms.ModelFormWidgetMixin,
                        CreatePopupMixin,
                        UpdateView):
        permission_required = f'{model_name}.change_{model_name}'
        model = apps.get_model(f'{__package__}.{model_name}')
        template_name = select_template(
            [f'{model_name}_create.html', 'create.html']).template.name
        success_url = f'/{model_name}'
        exclude = EXCLUDE
        widgets = generate_widgets(model)

        def get_object(self, obj=model.objects.get(id=pk)):
            return obj
    return GenericUpdate.as_view()(request)


def delete(request, model_name, pk):
    try:
        mod = apps.get_model(f'{__package__}.{model_name}')
        obj = mod.objects.get(id=pk)
        if request.method == "DELETE":
            if request.user.has_perm(f'{model_name}.delete_{model_name}'):
                obj.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False,
                                     'error': 'Unauthorized'})
        elif request.method == "GET":
            return details_view(request, model_name, pk)
    except:
        pass
