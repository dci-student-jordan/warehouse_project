from django import forms
from .models import Item, Employee


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            'date_of_stock': forms.DateInput(attrs={'type': 'date'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize widgets as needed
        self.fields['date_of_stock'].widget.attrs.update({
            'class': 'datepicker',
            'placeholder': 'Select a date',
        })