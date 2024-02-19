from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'  # You can specify the fields you want to include here if you don't want all fields
        # exclude = ["state", "category"]
        widgets = {
            'date_of_stock': forms.DateInput(attrs={'type': 'date'})
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize widgets as needed
        self.fields['date_of_stock'].widget.attrs.update({
            'class': 'datepicker',
            'placeholder': 'Select a date',
        })
        state_choices =self.instance.get_state_choices()
        cat_choices = self.instance.get_category_choices()
        print("SETTING:\nSTATE:", state_choices, "\nCATEGORIES:", cat_choices)
        self.fields['state'].choices = state_choices
        self.fields['category'].choices = cat_choices