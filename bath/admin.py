from django.contrib import admin

from bath.models import Appointment, Customer, Item


class ItemAdminInline(admin.TabularInline):
    model = Item


class CustomerAdminInline(admin.TabularInline):
    model = Customer


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'date',
        'start_time',
        'end_time',
        'status',
        'tag',
        'prepayment',
    )
    inlines = [ItemAdminInline]
    search_fields = ('start_time',)


# @admin.register(Service)
# class ServiceAdmin(admin.ModelAdmin):
#     list_display = (
#         'name',
#         'amount',
#         'measurement_unit',
#         'price',
#         'full_price',
#         'description',
#     )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'surname',
        'email',
        'phone',
    )


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'appointments',
        'rotenburo',
        'birch_broom',
        'oak_broom',
        'bed_sheet',
        'towel',
        'robe',
        'slippers',
    )
    readonly_fields = ('appointments',)
