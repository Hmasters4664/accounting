# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.http import is_safe_url
import csv
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.views.generic.base import View, TemplateView
from django.core import serializers
import json
from .models import Book,Records
from django.views.generic.list import ListView
from django.views.generic import UpdateView
#from .background import hello
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
import xlwt
import xlrd
import magic
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.conf import settings
import uuid
from django.urls import reverse_lazy
from .forms import BookForm
from bootstrap_modal_forms.generic import BSModalCreateView
from django.views.generic import TemplateView
from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView


class Main(TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'index.html'


class BookListJson(BaseDatatableView):
    model = Book
    columns = ['date_created', 'transaction_type', 'description', 'amount', 'name', 'transaction_date']
    order_columns = ['transaction_date', 'date_created',  'amount', 'transaction_type', 'description', 'name']

    def filter_queryset(self, qs):
        sSearch = self.request.GET.get('search[value]', None)
        if sSearch:
            print(sSearch)
            qs = qs.filter(Q(name__istartswith=sSearch) | Q(description__istartswith=sSearch))
        return qs


class BookEntryView(BSModalCreateView):
    template_name = 'form.html'
    form_class = BookForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')


