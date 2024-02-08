# forms.py
from django import forms
from .models import Employee, Contact
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    template_name = "registration/signup.html"
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Add class to prevent mouseout in script.js
            existing_classes = field.widget.attrs.get('class', '')
            new_class = 'keep_alive'
            updated_classes = f'{existing_classes} {new_class}'.strip()
            field.widget.attrs['class'] = updated_classes




class LoginForm(forms.ModelForm):
    template_name = "registration/login.html"
    
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Add class to prevent mouseout in script.js
            existing_classes = field.widget.attrs.get('class', '')
            new_class = 'keep_alive'
            updated_classes = f'{existing_classes} {new_class}'.strip()
            field.widget.attrs['class'] = updated_classes



class ContactForm(forms.ModelForm):
    template_name = "registration/contact.html"

    class Meta:
        model = Contact
        exclude = ["user"]
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Add class to prevent mouseout in script.js
            existing_classes = field.widget.attrs.get('class', '')
            new_class = 'keep_alive'
            updated_classes = f'{existing_classes} {new_class}'.strip()
            field.widget.attrs['class'] = updated_classes
