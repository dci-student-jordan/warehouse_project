from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, UpdateView
from django.views.generic.base import TemplateView
from .forms import ContactForm, LoginForm, CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms import Form
from .models import Item, Employee
from django.contrib.auth import login, authenticate, logout

# Create your views here.

def menu_links_style(exclude):
    links = [
        {"link":("index", []), "name":"Home", "menu":[{"link":("about", []), "name":"About"}]},
        {"link":("warehouse", "EU"), "name":"Awarehouse", "menu":[{"link":("products", "EU"), "name":"Products"}]},
        {"link":("warehouse", "USA"), "name":"Bewarehouse", "menu":[{"link":("products", "USA"), "name":"Products"}]},
        {"link":("warehouse", "ASIA"), "name":"Seewarehouse", "menu":[{"link":("products", "ASIA"), "name":"Products"}]},
        {"link":("warehouse", "INDIA"), "name":"Dewarehouse", "menu":[{"link":("products", "INDIA"), "name":"Products"}]}
    ]
    def un_menu(link:dict):
        if link["link"] == exclude:
            link = link["menu"][0]
        if "menu" in link.keys():
            link["menu"] = [] if link["menu"][0]["link"] == exclude else link["menu"]
        return link
    links = [un_menu(link) for link in links]
    stc = "a" if "EU" in exclude else \
        "b" if "USA" in exclude else \
        "c" if "ASIA"  in exclude else "d"
    style = f'warehouses/css/style_{stc}ware.css'

    continent = "Europe" if stc == "a" else \
        "the United States of America" if stc == "b" else \
            "Asia" if stc == "c" else "India"

    return links, style, continent


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

    # def get_initial(self):
    #     initial = super().get_initial()
    #     if not initial:
    #         emps = Employee.objects.all()
    #         initial = emps.__dict__
    #     return initial


class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("about")

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
            return super().form_valid(form)
        else:
            # Handle invalid login
            return self.form_invalid(form)
    
    def form_invalid(self, form: Any) -> HttpResponse:
        print("INVALID FORM: ", form.errors)
        return super().form_invalid(form)


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
            self.success_url = self.request.GET.get('next', '/')

        return response
    
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

def signup_html(request):
    log_type = request.path.split('/')[-1]
    # form = SignUpForm() if log_type == "signup" else LoginForm()
    template = f"registration/{log_type}.html"
    return render(request, template, {})

class RegisterView(TemplateView):
    template_name = "registration/reg_container.html"
    # form_class = ContactView
    # success_url = reverse_lazy("index")

    # def form_valid(self, form):
    #     form.save()
    #     print("saved")
    #     username = form.cleaned_data['username']
    #     password = form.cleaned_data['password']
    #     user = authenticate(username=username, password=password)

    #     if user is not None:
    #         login(self.request, user)
    #         if user.is_authenticated:
    #             print("logged in")
    #             self.success_url = super().render_to_response(self.get_context_data())
    #             # return redirect(next_url)
    #         return super().render_to_response(self.get_context_data())
    #     else:
    #         # Handle invalid login
    #         return super().render_to_response(self.get_context_data())
    
    # def form_invalid(self, form: BaseModelForm) -> HttpResponse:
    #     print("FORM INVALID:", form)
    #     return super().form_invalid(form)
    
    
def get_reg_from_request(request):
        view = RegisterView.as_view()
        # Render the view and get the response content
        response = view(request)
        return response.render().content


class Index(TemplateView):
    template_name = "main.html"
    links, style, continent = menu_links_style(("index", []))
    
    def get_context_data(self):
        context = {
            "reg": get_reg_from_request(self.request),
            "links": self.links,
            "title": "shopping 2.0",
            "header_text": "Welcome to shopping 2.0",
            "content_text": ["The future of social marketing."]
        }
        return context


class About(TemplateView):
    template_name = "about.html"
    links, style, continent = menu_links_style(("about", []))
    def get_context_data(self):
        return {
            "reg": get_reg_from_request(self.request),
            "links": self.links,
            "title":"about shopping 2.0",
            "header_text":"about us",
            "content_text":["We believe in humanity to be able to stop the waste of all goods we're provided.", 
                    "We refurbish products and provide them to prices you can set yourself.",
                    "We expect everybody to be able to value what he deserves.",
                    "We want everybody to be able to get what's needed.",
                    " "
                    "You can consider your payment as appreciation of the product and our imparting.",
                    "If you can afford feel free to consider the price you pay as a donation for others who own less.",
                    "If you don't have much and want to get a lot please give a reasonable comment on why.",
                    "Avarice will never hurt us, but probably you."]
        }

class Warehouse(TemplateView):
    template_name = "warehouse.html"
    def get_context_data(self, location):
        links, style, continent = menu_links_style(("warehouse", location))
        return {
            "reg": get_reg_from_request(self.request),
            "style":style,
            "links": links,
            "title":f"{'A' if location == 'EU' else 'B' if location == 'USA' else 'C' if location == 'ASIA' else 'D'}-Warehouse {location}",
            "header_text":f"Shopping 2.0 in the {location}",
            "content_text":[f"Explore our shop in {continent}.",
                "Our offers are collected from donations, private people, misproductions and so on.",
                "You define what to pay.",
                "Please place reasonable prices and comment on why in case you cannot."]
        }

class Products(TemplateView):
    template_name = "warehouse.html"
    def get_context_data(self, location):
        links, style, continent = menu_links_style(("products", location))
        wh = 1 if location == "EU" else 2 if location == "USA" else 3 if location == "ASIA" else 4
        content = Item.objects.filter(warehouse=wh)
        return {
            "reg": get_reg_from_request(self.request),
            "style":style,
            "links": links,
            "title":f"{'A' if location == 'EU' else 'B' if location == 'USA' else 'C' if location == 'ASIA' else 'D'}-Warehouse {location}",
            "header_text":f"Products in {location}",
            "content_text":[f"Heres a list of all Products in {continent}:"],
            "content":content
        }