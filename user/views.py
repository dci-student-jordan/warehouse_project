from typing import Any
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import CreateView, FormView, UpdateView
from .forms import ContactForm, LoginForm, CustomUserCreationForm, add_class_to_fields, ConnectEmployeeToUserForm, ReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.template.context_processors import csrf
from django.core.exceptions import ValidationError
from warehouses.models import Employee, EmployeeWorkingHours, ItemEdit, ItemOrder, Contact, Communication



class ContactView(LoginRequiredMixin, FormView):
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
        return json_response(ContactForm(), csrf(self.request)['csrf_token'], 'contact', self.get_context_data(message=f"Your message has been submitted successfully."))
    
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

    def form_valid(self, form):
        given_password = form.cleaned_data['password']
        emp = get_object_or_404(Employee, name=self.request.user.username)
        if emp:
            if emp.password == given_password:
                emp.user = self.request.user
                emp.save()
                print("Stored Emp")
                make_staff = User.objects.get(pk=self.request.user.pk)
                make_staff.is_staff = True
                make_staff.save()

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
        super().form_valid(form)
        form.save()
        
        # Log in the user after successful registration
        login(self.request, self.object)
        if self.request.user.is_authenticated and offer_employee_status(self.request.user):
            return JsonResponse({"html":"redirect", "redirect_url": reverse("connect_employee")})
        else:
            return JsonResponse({"html":""})
    
    def form_invalid(self, form):
        return json_response(form, csrf(self.request)['csrf_token'], 'signup', self.get_context_data())


class UpdateUserView(LoginRequiredMixin, UpdateView):    
    model = User
    success_url = reverse_lazy("index")
    template_name = "registration/update.html"
    fields = ('username', 'first_name', 'last_name', 'email')

    def post(self, request, *args, **kwargs):
        if 'message' in request.POST:
            print("HERE, PLEASE")
            form = ReplyForm(request.POST)
            message = form.cleaned_data['message']
            contact_id = kwargs.get('contact_id')
            contact = get_object_or_404(Contact, pk=contact_id)
            communication = Communication.objects.create(
                user=self.request.user,
                message=message
            )
            contact.communications.add(communication)
            # super().form_valid(form)
            return redirect('thanks', args=['message'])
        else:
            return super().post(request, *args, **kwargs)

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
    
    def form_valid(self, form):
        super().form_valid(form)
        return json_response(form, csrf(self.request)['csrf_token'], 'update', self.get_context_data(message="Your account data have been updated successfully."))
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        if "message" in kwargs.keys():
            context["message"] = kwargs["message"]
        user = self.request.user
        if user.is_authenticated:
            reply = False
            if user.is_staff:
                employee = Employee.objects.filter(user_id=user.pk).first()

                if employee:
                    context["working_hours"] = EmployeeWorkingHours.objects.filter(employee=employee).order_by("week_day")
                    context["edits"] = ItemEdit.objects.filter(employee=employee).order_by("-edited_at")[:5]
                    context["orders"] = ItemOrder.objects.filter(employee=employee).order_by("-ordered_at")[:5]
                    context["contacts"] = Contact.objects.filter(employee=employee)
                    if context["contacts"]:
                        reply = True
            context["communications"] = Contact.objects.filter(user=user)
            if context["communications"]:
                reply = True
            if reply and not "reply_form" in context.keys():
                context['reply_form'] = ReplyForm()


        return context
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    
def reply_to_contact(request, contact_id):
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            contact = get_object_or_404(Contact, pk=contact_id)
            communication = Communication.objects.create(
                user=request.user,
                message=message
            )
            contact.communications.add(communication)
            return redirect(reverse_lazy('thanks', args=['message']))
