from django import forms
from .models import Appointment, Customer, Item, Product
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rotenburo'].label = 'Ротенбуро'

    def set_label_rotenburo(self, x):
        self.fields['rotenburo'].label = f'Ротенбуро {x}р/ч'

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
                attrs={'placeholder': 'Ротенбуро:   кол. часов'}),
            'birch_broom': forms.TextInput(
                attrs={'placeholder': 'Веник берёза 300р/шт. :    штук'}),
            'oak_broom': forms.TextInput(
                attrs={'placeholder': 'Веник дуб 300р/шт. :       штук'}),
            'bed_sheet': forms.TextInput(
                attrs={'placeholder': 'Простыня 100р/шт. :        штук'}),
            'towel': forms.TextInput(
                attrs={'placeholder': 'Полотенце 100р/шт. :       штук'}),
            'robe': forms.TextInput(
                attrs={'placeholder': 'Халат 100р/шт. :           штук'}),
            'slippers': forms.TextInput(
                attrs={'placeholder': 'Тапки 100р/шт. :       кол. пар'}),

        }
        labels = {'birch_broom': '', 'rotenburo': '',
                  'oak_broom': '',
                  'bed_sheet': '',
                  'towel': '',
                  'robe': '',
                  'slippers': '',
                  }


class CustomerForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email'}),
        label=''
    )

    class Meta:
        model = Customer
        fields = ('email', 'name', 'phone')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон'})
        }
        labels = {'name': '', 'email': '', 'phone': ''}


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(label='', required=False,
                                  widget=forms.TextInput(attrs={
                                      'placeholder': 'шт.'}))
