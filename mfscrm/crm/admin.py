import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Customer, Service, Product


def make_published(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response


make_published.short_description = "Export as CSV file"


class CustomerList(admin.ModelAdmin):
    list_display = ('cust_name', 'organization', 'phone_number')
    list_filter = ('cust_name', 'organization')
    search_fields = ('cust_name',)
    ordering = ['cust_name']
    actions = [make_published]


class ServiceList(admin.ModelAdmin):
    list_display = ('cust_name', 'service_category', 'setup_time')
    list_filter = ('cust_name', 'setup_time')
    search_fields = ('cust_name',)
    ordering = ['cust_name']


class ProductList(admin.ModelAdmin):
    list_display = ('cust_name', 'product', 'pickup_time')
    list_filter = ('cust_name', 'pickup_time')
    search_fields = ('cust_name',)
    ordering = ['cust_name']


admin.site.register(Customer, CustomerList)
admin.site.register(Service, ServiceList)
admin.site.register(Product, ProductList)
