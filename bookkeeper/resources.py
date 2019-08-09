from import_export import resources
from .models import Book

class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        fields = ('acquisition_date', 'asset_name', 'description', 'asset_type', 'asset_barcode', 'asset_serial_number',
                  'asset_status', 'asset_user', 'asset_department', 'purchase_value', 'residual_value',
                  'life_expectancy', )