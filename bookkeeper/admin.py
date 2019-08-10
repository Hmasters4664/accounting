from django.contrib import admin
from organizations.models import (Organization, OrganizationUser,
    OrganizationOwner)
from bookkeeper.models import Company, CompanyUser, CompanyOwner

admin.site.register(Company)
admin.site.register(CompanyUser)
admin.site.register(CompanyOwner)