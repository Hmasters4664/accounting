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
# Create your models here.

TRANSACTIONTYPE = (
        ('INCOME', 'INCOME'),
        ('EXPENSE', 'EXPENSE'),
    )


class Book(models.Model):
    date = models.DateField(default=datetime.date.today)
    transaction_type = models.CharField(choices=TRANSACTIONTYPE, max_length=9, validators=[validate_characters], )

    











