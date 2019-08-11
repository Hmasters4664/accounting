from django.forms import ModelForm
from bookkeeper.models import *
from bootstrap_modal_forms.forms import BSModalForm


class BookForm(BSModalForm):
    class Meta:
        model = Book
        fields = ['transaction_type', 'description', 'amount', 'name', 'transaction_date']
