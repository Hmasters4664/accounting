# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
import datetime
from django.conf import settings
from .managers import UserManager
from django.utils.translation import ugettext_lazy as _
from .validators import validate_characters, check_negative_number, check_zero_number
from django.contrib.auth.models import User
from organizations.models import Organization, OrganizationUser
from django.contrib.auth.models import Permission
from organizations.base import (
    OrganizationBase,
    OrganizationUserBase,
    OrganizationOwnerBase,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

TRANSACTIONTYPE = (
        ('INCOME', 'INCOME'),
        ('EXPENSE', 'EXPENSE'),
    )


class Book(models.Model):
    date_created = models.DateField(default=datetime.date.today)
    #organisation = models.ForeignKey("Company", on_delete=models.PROTECT, blank=True, null=True)
    transaction_type = models.CharField(choices=TRANSACTIONTYPE, max_length=9, validators=[validate_characters], )
    description = models.TextField(max_length=150, validators=[validate_characters], )
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=000.00,
                                validators=[check_negative_number], )
    name = models.CharField(max_length=30, validators=[validate_characters], )
    transaction_date = models.DateField(default=datetime.date.today)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=000.00,
                                 validators=[check_negative_number], )

    def natural_key(self):
        return self.my_natural_key


class Records(models.Model):
    description = models.TextField(max_length=1000)
    date = models.DateField(default=datetime.date.today)


class Company(OrganizationBase):
    street_address = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")


class CompanyUser(OrganizationUserBase):
    user_type = models.CharField(max_length=1, default="")
    permissions = models.ManyToManyField(Permission, blank=True)


class CompanyOwner(OrganizationOwnerBase):
    pass




    











