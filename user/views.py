from typing import Any
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, UpdateView
from .forms import ContactForm, LoginForm, CustomUserCreationForm, add_class_to_fields
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.template.context_processors import csrf
from django.core.exceptions import ValidationError



class ContactView(FormView):
    template_name = 'registration/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy("index")

    def get_success_url(self) -> str:
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return super().get_success_url()

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form: Any):
        print("Invalid CONTACT")
        return super().form_invalid(form)


class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("index")


    def get_success_url(self) -> str:
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return super().get_success_url()

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            # force page reload
            return JsonResponse({"html":""})
        else:
            # Handle invalid login
            form.add_error(None, ValidationError("Invalid username or password."))
            return self.form_invalid(form)

    def form_invalid(self, form):
        return json_response(form, csrf(self.request)['csrf_token'], 'login', self.get_context_data())


def json_response(form, csrf_token, template, context, view=ContactView()):
    context["form"] = form
    context["csrf_token"] = csrf_token
    context["view"] = view
    html = render_to_string(f"registration/{template}.html", context)
    return JsonResponse({'html': html})

def custom_logout(request):
    logout(request)
    return redirect("login")
    

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("index")
    template_name = "registration/signup.html"

    def get_success_url(self) -> str:
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return super().get_success_url()

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Log in the user after successful registration
        login(self.request, self.object)
        if self.request.user.is_authenticated:
            return json_response(ContactForm(), csrf(self.request)['csrf_token'], 'contact', self.get_context_data())

        return response
    
    def form_invalid(self, form):
        return json_response(form, csrf(self.request)['csrf_token'], 'signup', self.get_context_data())
    
class UpdateUserView(LoginRequiredMixin, UpdateView):    
    model = User
    success_url = reverse_lazy("index")
    template_name = "registration/update.html"
    fields = ('username', 'first_name', 'last_name', 'email')

    def get_success_url(self) -> str:
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return super().get_success_url()
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Add class to form fields
        form.fields = add_class_to_fields(form.fields)
        return form

    def form_invalid(self, form):
        return json_response(form, csrf(self.request)['csrf_token'], 'update', self.get_context_data())