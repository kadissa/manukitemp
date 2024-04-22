from django import forms
from .models import Appointment, Customer, Item
from crispy_forms.helper import FormHelper


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = (
            'date',
            'start_time',
            'end_time',
        )


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            'rotenburo',
            'birch_broom',
            'oak_broom',
            'bed_sheet',
            'towel',
            'robe',
            'slippers',
        )


class CustomerForm(forms.ModelForm):
    helper = FormHelper()

    class Meta:
        model = Customer
        fields = ('name', 'email', 'phone')
