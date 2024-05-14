from django.contrib import admin

from bath.models import Appointment, Customer, Item


class AppointmentAdminInline(admin.TabularInline):
    model = Appointment


class CustomerAdminInline(admin.TabularInline):
    model = Customer


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'items',
        'customer',
        'date',
        'start_time',
        'end_time',
        # 'status',
        # 'tag',
        # 'prepayment',
    )
    # inlines = [ItemAdminInline, CustomerAdminInline]
    search_fields = ('start_time',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'surname',
        'email',
        'phone',
    )
    inlines = [AppointmentAdminInline]

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'rotenburo',
        'birch_broom',
        'oak_broom',
        'bed_sheet',
        'towel',
        'robe',
        'slippers',
    )
    inlines = [AppointmentAdminInline]