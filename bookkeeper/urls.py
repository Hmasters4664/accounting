from django.conf.urls import url
from django.urls import include, re_path, path
from organizations.backends import invitation_backend
from bookkeeper.views import Main, BookListJson, BookEntryView, BookUpdateView

urlpatterns = [
    path('', Main.as_view(), name='index'),
    re_path(r'^BookList', BookListJson.as_view(), name='BookList'),
    re_path(r'^accounts/', include('organizations.urls')),
    re_path(r'^invitations/', include(invitation_backend().get_urls())),
    re_path(r'^create/', BookEntryView.as_view(), name='create_book'),
    re_path(r'^update/(?P<pk>\d+)/', BookUpdateView.as_view(), name='update_book'),

]