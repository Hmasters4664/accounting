from import_export import resources
from .models import Book


class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        fields = ('transaction_date', 'transaction_type', 'description', 'amount', 'name', 'total', )
