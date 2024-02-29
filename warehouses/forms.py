from django import forms
from .models import Item


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


class OrderItemsForm(forms.Form):
    
    amount = forms.IntegerField(label='Amount', min_value=1)

    def __init__(self, *args, **kwargs):
        location = kwargs.pop('location')
        state = kwargs.pop('state')
        category = kwargs.pop('category')
        super().__init__(*args, **kwargs)
        
        # Query the database to get the maximum available amount of items
        # matching the provided state, category, and location
        max_available_amount = Item.objects.filter(
            state=state, category=category
        ).count()

        # Update the form field to set the maximum value
        self.fields['amount'].widget.attrs['max'] = max_available_amount

