# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.http import is_safe_url
import csv
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Asset, Location,Records
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.views.generic.base import View, TemplateView
from django.core import serializers
import json
from .forms import AssetForm, LocationForm, RejectionForm
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
from django.db.models import Q
import xlwt
import xlrd
from .resources import AssetResource
from tablib import Dataset
from import_export import resources
import magic
from django.core.files.storage import default_storage
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.conf import settings

import uuid


# Create your views here.
class addAsset(LoginRequiredMixin, FormView):
    model= Asset
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name= 'assets.html'
    form_class = AssetForm
    success_url = '/assets/'
    def form_valid(self,form):
        asset = form.save(commit=False)
        asset.asset_owner = self.request.user
        asset.save()
        rec = Records(description='user: '+self.request.user.get_employee_id() +
                                  ' added a new asset with id '+str(asset.asset_id))
        rec.save()
        return super().form_valid(form)
########################################################################################################################


class addLocation(LoginRequiredMixin, FormView):
    model=Location
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name= 'addlocation.html'
    form_class = LocationForm
    success_url = '/assets/'

    def form_valid(self,form):
        form.save()
        return super().form_valid(form)

#######################################################################################################################


class main(LoginRequiredMixin, ListView):
    model = Asset
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name= 'index.html'
    context_object_name = 'assets'
    paginate_by = 10
    Asset.objects.all()
########################################################################################################################
@login_required
def Search(request):
    object_list = Asset.objects.filter(asset_name__startswith=request.GET.get('search')).values("asset_id",
                                                     "acquisition_date", "asset_name",
                                                     "description", "asset_type", "asset_barcode",
                                                     "asset_serial_number",
                                                     "asset_location", "asset_status", "asset_owner",'asset_user',
                                                    'asset_is_rejected')

    jason = list(object_list)
    print(jason)
    return JsonResponse(jason, safe=False)

########################################################################################################################
@login_required
def approve(request,pk):
    if request.user.is_manager:
        asset = get_object_or_404(Asset, pk=pk)
        asset.asset_is_approved=True
        asset.save()
        rec = Records(description='user: ' + request.user.get_employee_id() + ' approved an asset with id ' + str(
            asset.asset_id))
        rec.save()
        return redirect('pending')

    else:
        return HttpResponseForbidden()
#######################################################################################################################


class editAsset(LoginRequiredMixin, UpdateView):
    model = Asset
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'assets.html'
    form_class = AssetForm
    success_url = '/assets/'

    def form_valid(self, form):
        asset = form.save(commit=False)
        date = datetime.now()
        dates = date.strftime("%Y-%m-%d")
        asset.modified_date = dates
        asset.asset_is_rejected = False
        asset.asset_is_approved = False
        asset.save()
        rec = Records(description='user: ' + self.request.user.get_employee_id() + ' modified an asset with id ' + str(
            asset.asset_id))
        rec.save()
        return super().form_valid(form)


########################################################################################################################


class Login(FormView):
    template_name = 'login.html'
    success_url = '/assets/'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(Login, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to
########################################################################################################################


class LocationList(LoginRequiredMixin, ListView):
    model = Location
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name= 'location.html'
    context_object_name = 'locations'
    paginate_by = 10
    queryset = Location.objects.all()

########################################################################################################################


class ApprovalList(LoginRequiredMixin, ListView):
    model = Asset
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'approval_page.html'
    paginate_by = 10

    def get_context_data(self, *, assets=None, **kwargs):
        context = super(ApprovalList, self).get_context_data()
        if self.request.user.is_manager:
            context['assets'] = Asset.objects.filter(asset_is_approved=False, asset_is_rejected=False)

        else:
            context['assets'] = ''

        return context

########################################################################################################################
@login_required
def SpecialSearch(request):

    if request.user.is_manager:
        object_list = Asset.objects.filter(asset_name__startswith=request.GET.get('search')).\
            filter(asset_is_approved=False, asset_is_rejected=False)\
                                                    .values("asset_id",
                                                     "acquisition_date", "asset_name",
                                                     "description", "asset_type", "asset_barcode",
                                                     "asset_serial_number",
                                                     "asset_location", "asset_status", "asset_owner")

    else:
        object_list = Asset.objects.filter(asset_name__startswith=request.GET.get('search')).\
            filter(asset_is_approved=False, asset_is_rejected=True, asset_owner=request.user)\
                                                    .values("asset_id",
                                                     "acquisition_date", "asset_name",
                                                     "description", "asset_type", "asset_barcode",
                                                     "asset_serial_number",
                                                     "asset_location", "asset_status", "asset_owner")

    jason = list(object_list)
    return JsonResponse(jason, safe=False)

########################################################################################################################
@login_required
def logout(request):
    success_url = '/login/'
    redirect_field_name = REDIRECT_FIELD_NAME
    auth_logout(request)

    return redirect(success_url)
########################################################################################################################
@login_required
def to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="assets.csv"'
    writer = csv.writer(response)
    writer.writerow(['Asset Name', 'Acquisition Date', 'Description', 'Asset Type','Asset Barcode','Serial Number',
                     'Purchase Value','Current Value','Status','Date Of Value Calculation','Depreciation Method '])

    assetslist=Asset.objects.filter(asset_is_approved=True).values_list("asset_name",'acquisition_date','description',
                                                                   'asset_type','asset_barcode','asset_serial_number',
                                                                   'purchase_value','current_value','asset_status',
                                                                   'currentVal_date','depr_model')

    for asset in assetslist:
        writer.writerow(asset)

    return response
########################################################################################################################
@login_required
def to_xlsx(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="asset.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Assets')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Asset Name', 'Acquisition Date', 'Description', 'Asset Type','Asset Barcode','Serial Number',
                     'Purchase Value','Current Value','Status','Date Of Value Calculation','Depreciation Method ']

    assetslist = Asset.objects.filter(asset_is_approved=True).values_list("asset_name",'acquisition_date','description',
                                                                   'asset_type','asset_barcode','asset_serial_number',
                                                                   'purchase_value','current_value','asset_status',
                                                                   'currentVal_date','depr_model')

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    for row in assetslist:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
########################################################################################################################


class BulkUpload(LoginRequiredMixin, View):
    template_name = 'upload.html'
    success_url = '/assets/'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        new_assets = request.FILES['myfile']

        if new_assets.size > 1048576:
            return render(request,'500_error.html')

        mime = magic.from_buffer(new_assets.read(), mime=True)

        if (mime == 'application/vnd.ms-excel'):

            new_assets.seek(0)
            filename = str(uuid.uuid4())+'.xls'
            file_name = default_storage.save(filename, ContentFile(new_assets.read()))
            data = xlrd.open_workbook(settings.MEDIA_ROOT +'/'+file_name)
            table = data.sheets()[0]
            for i in range(1,  table.nrows):
               row = table.row(i)
               seconds =(row[0].value - 25569)*86400.0
               date = datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d')
               barcode = str(row[4].value)
               newasset = Asset(acquisition_date=date,	asset_name=row[1].value, description=row[2].value,
                              asset_type=row[3].value,
                               asset_barcode=row[4].value, asset_serial_number=row[5].value, asset_status=row[6].value,
                              asset_user=row[7].value,
                               asset_department=row[8].value,	purchase_value=row[9].value,
                              residual_value=row[10].value,
                               life_expectancy =row[11].value, depr_model=row[12].value,
                              asset_owner = self.request.user)

               try:
                newasset.full_clean()
               except ValidationError as e:
                print(e)
                return render(request, '500_error.html')
               newasset.save()
        else:
            return render(request, '500_error.html')

        return redirect(self.success_url)
########################################################################################################################
@login_required
def noficications(request):
    if request.user.is_manager:
        AssetsList = Asset.objects.filter(asset_is_approved=False, asset_is_rejected=False).values("asset_id",
                                                     "acquisition_date", "asset_name",
                                                     "description", "asset_type", "asset_barcode",
                                                     "asset_serial_number",
                                                     "asset_location", "asset_status", "asset_owner")\
                     .order_by('-acquisition_date')[:5]
    else:
        AssetsList = Asset.objects.filter(asset_is_approved=False, asset_is_rejected=True, asset_owner=request.user)\
            .values("asset_id",
                                                                                                   "acquisition_date",
                                                                                                   "asset_name",
                                                                                                   "description",
                                                                                                   "asset_type",
                                                                                                   "asset_barcode",
                                                                                                   "asset_serial_number",
                                                                                                   "asset_location",
                                                                                                   "asset_status",
                                                                                                   "asset_owner") \
            .order_by('-acquisition_date')[:5]


    jayson = list(AssetsList)
    return JsonResponse(jayson, safe=False)

########################################################################################################################
@login_required
def locationSearch(request):
    object_list = Location.objects.filter(city__startswith=request.GET.get('search'))\
                                                    .values("city", "province",
                                                     "country", "building", "floor",
                                                     "adress")

    jason = list(object_list)
    return JsonResponse(jason, safe=False)
########################################################################################################################


class RejectAsset(LoginRequiredMixin, UpdateView):
    model = Asset
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'assets.html'
    form_class = RejectionForm
    success_url = '/assets/'


    def form_valid(self, form):
        if self.request.user.is_manager:
            asset = form.save(commit=False)
            asset.asset_is_rejected = True
            asset.asset_is_approved = False
            asset.save()
            rec = Records(description='user: ' + self.request.user.get_employee_id() + ' rejected an asset with id ' + str(
                asset.asset_id))
            rec.save()
            return super().form_valid(form)
        else:
            return HttpResponseForbidden()

########################################################################################################################


@login_required
def getname(request):
    name = request.user.get_full_name()
    return JsonResponse(name, safe=False)
########################################################################################################################


@login_required(login_url='/login/')
def pending(request):
    if request.user.is_manager:
        assets = Asset.objects.filter(asset_is_approved=False, asset_is_rejected=False)
        return render(request, 'approval_page.html', {'assets': assets})
    else:
        assets = Asset.objects.filter(asset_is_approved=False, asset_is_rejected=True, asset_owner=request.user)
        return render(request, 'rejection_page.html', {'assets': assets})
########################################################################################################################
