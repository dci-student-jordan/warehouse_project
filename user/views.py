from typing import Any
from django.template.loader import render_to_string
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, FormView, UpdateView
from .forms import ContactForm, LoginForm, CustomUserCreationForm, add_class_to_fields, ConnectEmployeeToUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.template.context_processors import csrf
from django.core.exceptions import ValidationError
from warehouses.models import Employee



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


class LoginRequiredView(FormView):
    template_name = 'registration/login_required.html'
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
            return json_response(ContactForm(), csrf(self.request)['csrf_token'], 'contact', self.get_context_data())


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
            if self.request.user.is_authenticated and offer_employee_status(self.request.user):
                super().form_valid(form)
                return JsonResponse({"html":"redirect", "redirect_url": reverse("connect_employee")})
            else:
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

def offer_employee_status(user):
    if Employee.objects.filter(user=user).exists():
        print(f"{user} has employee status")
        return False
    elif Employee.objects.filter(name=user):
        # offer employee status
        print(f"offer employee status to {user}")
        return True
    else:
        print(f"{user} is no employee")
        return False


class ConnectEmployeeView(LoginRequiredMixin, FormView):
    form_class = ConnectEmployeeToUserForm
    success_url = reverse_lazy("index")
    template_name = "registration/connect_employee.html"

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        print("connectPOST:", request.user, args, kwargs)
        return super().post(request, *args, **kwargs)
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        print("connectGET:", request.user, args, kwargs)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        given_password = form.cleaned_data['password']
        emp = get_object_or_404(Employee, name=self.request.user.username)
        if emp:
            if emp.password == given_password:
                emp.user = self.request.user
                emp.save()
                print("Stored Emp")
            else:
                print("Passwords not equal")
                raise ValidationError(f"That's not the right password, {self.request.user.username}.")
        else:
            print("Emp not found")

        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("Invalid:", form)
        return super().form_invalid(form)
    

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
        
        # Log in the user after successful registration
        login(self.request, self.object)
        if self.request.user.is_authenticated and offer_employee_status(self.request.user):
            super().form_valid(form)
            return JsonResponse({"html":"redirect", "redirect_url": reverse("connect_employee")})
        else:
            return super().form_valid(form)
    
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
    