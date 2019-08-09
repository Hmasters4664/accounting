from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager

# Create your models here.

DEPARTMENT = (
    ('I.T', 'I.T'),
    ('Finance', 'Finance'),
    ('Marketing', 'Marketing'),
    ('Sales', 'Sales'),
)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_manager = models.BooleanField(_('manger'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    employee_id = models.CharField(_('Employee ID'),max_length=50,blank=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['employee_id']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def get_employee_id(self):
        '''
        Returns the short name for the user.
        '''
        return self.employee_id
