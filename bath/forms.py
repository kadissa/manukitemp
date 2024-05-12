from django import forms
from .models import Appointment, Customer, Item
from crispy_forms.helper import FormHelper
from phonenumber_field.widgets import RegionalPhoneNumberWidget


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
        widgets = {
            'rotenburo': forms.TextInput(
                attrs={'placeholder': 'Ротенбуро: сколько часов'}),
            'birch_broom': forms.TextInput(
                attrs={'placeholder': 'Веник берёза:    штук'}),
            'oak_broom': forms.TextInput(
                attrs={'placeholder': 'Веник дуб:   штук'}),
            'bed_sheet': forms.TextInput(
                attrs={'placeholder': 'Простыня:   штук'}),
            'towel': forms.TextInput(
                attrs={'placeholder': 'Полотенце:    штук'}),
            'robe': forms.TextInput(
                attrs={'placeholder': 'Халат:   штук'}),
            'slippers': forms.TextInput(
                attrs={'placeholder': 'Тапки:   количество пар'}),

        }
        labels = {'birch_broom': '', 'rotenburo': '',
                  'oak_broom': '',
                  'bed_sheet': '',
                  'towel': '',
                  'robe': '',
                  'slippers': '',
                  }


class CustomerForm(forms.ModelForm):
    # helper = FormHelper()

    class Meta:
        model = Customer
        fields = ('name', 'email', 'phone')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            # 'phone': RegionalPhoneNumberWidget(),
        }
        labels = {'name': '', 'email': '', 'phone': ''}
