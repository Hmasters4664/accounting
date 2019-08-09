from django.conf.urls import url
from django.urls import include, re_path, path
from AMS import views
from AMS.views import addAsset, addLocation, main, editAsset,Login, LocationList,ApprovalList, BulkUpload, RejectAsset

urlpatterns = [
    path('', main.as_view(), name='index'),
    re_path(r'^login', Login.as_view(), name='login'),
    re_path(r'^assets', main.as_view(), name='main'),
    re_path(r'^add', addAsset.as_view(), name='add'),
    re_path(r'^location',addLocation.as_view(),name='location'),
    re_path(r'^search',views.Search,name='search'),
    re_path(r'^asset/(?P<pk>\d+)/',editAsset.as_view(),name='modify'),
    re_path(r'^Llist', LocationList.as_view(), name='Llist'),
    re_path(r'^pending', views.pending, name='pending'),
    re_path(r'^specialsearch',views.SpecialSearch,name='specialsearch'),
    re_path(r'^logout',views.logout,name='logout'),
    re_path(r'^approve/(?P<pk>\d+)/',views.approve,name='approve'),
    re_path(r'^reject/(?P<pk>\d+)/',RejectAsset.as_view(),name='reject'),
    re_path(r'^export/csv/$', views.to_csv, name='assets_to_csv'),
    re_path(r'^export/xlsx/$', views.to_xlsx, name='assets_to_xlsx'),
    re_path(r'^notifications', views.noficications, name='notifications'),
    re_path(r'^LSS', views.locationSearch, name='LSS'),
    re_path(r'^getname', views.getname, name='getname'),
    re_path(r'^XLSupload', BulkUpload.as_view(), name='xls_Upload')
]