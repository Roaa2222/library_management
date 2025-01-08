from django.contrib import admin
from .models import Book
from .models import Transaction


admin.site.register(Book)
admin.site.register(Transaction)
admin.site.site_header = 'Library_Management'
#admin.header.

# Register your models here.
