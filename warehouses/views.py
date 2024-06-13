# warehouses.views.py
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, FormView
from .models import Item, EmployeeWorkingHours, ItemEdit, Employee, ItemOrder
from .forms import ItemForm, OrderItemsForm
from django.db.models import Q, Count, Min, F
from django.db import transaction
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from user.custom_mixins import StaffRequiredMixin

# Create your views here.

def menu_links_style(exclude):
    links = [
        {"link":("index", ()), "name":"Home", "menu":[{"link":("index", ()), "name":"Home"}, {"link":("about", ()), "name":"About"}, {"link":("products", "ALL"), "name":"All Products"}, {"link":("search", "ALL"), "name":"Search all products"}, {"link":("filtered", ["ALL", "category"]), "name":"Search products by category"}, {"link":("filtered", ["ALL", "state"]), "name":"Search products by state"}]},
        {"link":("warehouse", "EU"), "name":"Awarehouse", "menu":[{"link":("warehouse", "EU"), "name":"Awarehouse Home"}, {"link":("products", "EU"), "name":"EU Products"}, {"link":("search", "EU"), "name":"Search EU products"}, {"link":("filtered", ["EU", "category"]), "name":"Search EU products by category"}, {"link":("filtered", ["EU", "state"]), "name":"Search EU products by state"}]},
        {"link":("warehouse", "USA"), "name":"Bewarehouse", "menu":[{"link":("warehouse", "USA"), "name":"Bewarehouse Home"}, {"link":("products", "USA"), "name":"USA Products"}, {"link":("search", "USA"), "name":"Search USA products"}, {"link":("filtered", ["USA", "category"]), "name":"Search USA products by category"}, {"link":("filtered", ["USA", "state"]), "name":"Search USA products by state"}]},
        {"link":("warehouse", "ASIA"), "name":"Seawarehouse", "menu":[{"link":("warehouse", "ASIA"), "name":"Seawarehouse Home"}, {"link":("products", "ASIA"), "name":"ASIA Products"}, {"link":("search", "ASIA"), "name":"Search ASIA products"}, {"link":("filtered", ["ASIA", "category"]), "name":"Search ASIA products by category"}, {"link":("filtered", ["ASIA", "state"]), "name":"Search ASIA products by state"}]},
        {"link":("warehouse", "INDIA"), "name":"Dewarehouse", "menu":[{"link":("warehouse", "INDIA"), "name":"Dewarehouse Home"}, {"link":("products", "INDIA"), "name":"INDIA Products"}, {"link":("search", "INDIA"), "name":"Search INDIA products"}, {"link":("filtered", ["INDIA", "category"]), "name":"Search INDIA products by category"}, {"link":("filtered", ["INDIA", "state"]), "name":"Search INDIA products by state"}]},
    ]
    def un_menu(link:dict):
        if "menu" in link.keys():
            link["menu"] = [l for l in link["menu"] if not l["link"] == exclude]
        elif link["link"] == exclude:
            menu = link["menu"][1:]
            link = link["menu"][0]
            link["menu"] = menu
        return link
    links = [un_menu(link) for link in links]
    if type(exclude[1]) == list:
        exclude = exclude[1]
    stc = "a" if "EU" in exclude else \
        "b" if "USA" in exclude else \
        "c" if "ASIA"  in exclude else \
        "d" if "INDIA"  in exclude else "e"
    style = f'warehouses/css/style_{stc}ware.css'

    continent = "Europe" if stc == "a" else \
        "the United States of America" if stc == "b" else \
            "Asia" if stc == "c" else "India" if stc == "d" \
            else "all our warehouses"

    return links, style, continent


class RegisterView(TemplateView):
    '''View containing registration etc'''
    template_name = "registration/reg_container.html"
    
def get_reg_from_request(request):
    view = RegisterView.as_view()
    # Render the view and get the response content
    response = view(request)
    if isinstance(response, TemplateResponse):
        return response.render().content
    else:
        # Handle non-TemplateResponse cases
        return response.content

class NotFound(TemplateView):
    template_name = "not_found.html"

class Index(TemplateView):
    template_name = "main.html"
    links, style, continent = menu_links_style(("index", ()))
    
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
    links, style, continent = menu_links_style(("about", ()))
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
        super().get_context_data()
        links, style, continent = menu_links_style(("warehouse", location))
        return {
            "reg": get_reg_from_request(self.request),
            "style":style,
            "links": links,
            "location":location,
            "title":f"{'A' if location == 'EU' else 'B' if location == 'USA' else 'C' if location == 'ASIA' else 'D'}-Warehouse {location}",
            "header_text":f"Shopping 2.0 in {continent}",
            "content_text":[f"Explore our shop in {continent}.",
                "Our offers are collected from donations, private people, misproductions and so on.",
                "You define what to pay.",
                "Please place reasonable prices and comment on why in case you cannot."]
        }

class Products(TemplateView):
    template_name = "warehouse.html"
    def get_context_data(self, location):
        links, style, continent = menu_links_style(("products", location))
        first_pk = F('id')
        if location == "ALL":
            content = Item.objects.filter(shipped=False).values("category", "state").annotate(count=Count('id'), pk=Min(first_pk)).distinct()
        else:
            wh = 1 if location == "EU" else 2 if location == "USA" else 3 if location == "ASIA" else 4
            content = Item.objects.filter(warehouse=wh, shipped=False).values("category", "state").annotate(count=Count('id'), pk=Min(first_pk)).distinct()
        return {
            "reg": get_reg_from_request(self.request),
            "style":style,
            "links": links,
            "location":location,
            "title":f"{'A' if location == 'EU' else 'B' if location == 'USA' else 'C' if location == 'ASIA' else 'D' if location == 'INDIA' else 'Your'}-Warehouse {location if location != 'ALL' else ''}",
            "header_text":f"Products in {continent}",
            "content_text":[f"Here is a list of all Products in {continent} ({len(content)} in total):"],
            "content":content
        }



class ProductDetailView(StaffRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = "product_detail.html"
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('thanks', args=["update"])

    def form_valid(self, form):
        self.object = form.save()
        emp = Employee.objects.filter(user_id=self.request.user.pk).first()
        ItemEdit.objects.create(employee=emp, item=self.object)
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content = self.get_object()
        wh = content.warehouse_id
        location = "EU" if wh == 1 else "USA" if wh == 2 else "ASIA" if wh == 3 else "INDIA" # if wh == 4 else "ALL"
        links, style, continent = menu_links_style(("product", location))
        context.update({
            "reg": get_reg_from_request(self.request),
            "style":style,
            "links": links,
            "location":location,
            "title":f"{'A' if location == 'EU' else 'B' if location == 'USA' else 'C' if location == 'ASIA' else 'D' if location == 'INDIA' else 'Your'}-Warehouse {location if location != 'ALL' else ''}",
            "header_text":f"Update Item #{content.pk} from {location}"
        })
        return context
    

class OrderView(LoginRequiredMixin, StaffRequiredMixin, FormView):
    template_name = 'product_order.html'
    form_class = OrderItemsForm
    success_url = reverse_lazy('thanks', args=["order"])

    @transaction.atomic
    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        items_to_order = Item.objects.filter(
            state=self.state, category=self.category, shipped=False
        )
        items_to_order = items_to_order.order_by('id')[:amount]
        emp = Employee.objects.filter(user_id=self.request.user.pk).first()
        item_order = ItemOrder.objects.create(employee=emp, amount=amount)
        for item in items_to_order:
            item_order.item.add(item)
            item.shipped = True
            item.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['location'] = self.kwargs.get('location')
        kwargs['state'] = self.kwargs.get('state')
        kwargs['category'] = self.kwargs.get('category')
        return kwargs

    def get_initial(self):
        self.location = self.kwargs.get('location')
        self.state = self.kwargs.get('state')
        self.category = self.kwargs.get('category')

        # Query the database to get the maximum available amount of items
        # matching the provided state, category, and location
        max_available_amount = Item.objects.filter(
            state=self.state, category=self.category, shipped=False
        ).count()

        return {'amount': max_available_amount}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location'] = self.location
        links, style, continent = menu_links_style(("product", self.location))
        context.update({
            "reg": get_reg_from_request(self.request),
            "style":style,
            "links": links,
            "location":self.location,
            "title":f"{'A' if self.location == 'EU' else 'B' if self.location == 'USA' else 'C' if self.location == 'ASIA' else 'D' if self.location == 'INDIA' else 'Your'}-Warehouse {self.location if self.location != 'ALL' else ''}",
            "header_text":f"Order Items from {self.location}",
            "product":f"'{self.state} {self.category}'"
        })
        return context

class Thanks(TemplateView):
    template_name = "thanks.html"

    def get_context_data(self, action, **kwargs):
        message = "Your order has been successfully placed." if action == "order" else \
                    "Your update is now stored in our database."  if action == "update" else \
                    "Your message has been transmitted successfully."
        context = super().get_context_data(**kwargs)
        context["message"] = message

        return context


class List_Filtered(TemplateView):
    template_name = "warehouse.html"
    def get_context_data(self, location, filter):
        links, style, continent = menu_links_style(("filtered", [location, filter]))
        if location == "ALL":
            content_links = Item.objects.filter(shipped=False).values(filter).annotate(count=Count('id')).distinct()
        else:
            wh = 1 if location == "EU" else 2 if location == "USA" else 3 if location == "ASIA" else 4
            content_links = Item.objects.filter(warehouse=wh, shipped=False).values(filter).annotate(count=Count('id')).distinct()
        return {
            "reg": get_reg_from_request(self.request),
            "style":style,
            "links": links,
            "location":location,
            "title":f"{'A' if location == 'EU' else 'B' if location == 'USA' else 'C' if location == 'ASIA' else 'D'}-Warehouse {location}",
            "header_text":f"Available {'categories' if filter == 'category' else 'states'} in {continent}",
            "content_text":[f"Here is a list of each {filter} available in {continent} ({len(content_links)} in total):"],
            "filtered_by": filter,
            "content_links": content_links
        }

class List_Items_Filtered(TemplateView):
    template_name = "warehouse.html"
    def get_context_data(self, location, filter, filter_string):
        links, style, continent = menu_links_style(("filtered", [location, filter]))
        args = {filter:filter_string}
        if location == "ALL":
            content = Item.objects.filter(shipped=False, **args)
        else:
            wh = 1 if location == "EU" else 2 if location == "USA" else 3 if location == "ASIA" else 4
            content = Item.objects.filter(warehouse=wh, shipped=False, **args)
        return {
            "reg": get_reg_from_request(self.request),
            "style":style,
            "links": links,
            "location":location,
            "title":f"{'A' if location == 'EU' else 'B' if location == 'USA' else 'C' if location == 'ASIA' else 'D'}-Warehouse {location}",
            "header_text":f"Items of {filter} '{filter_string}' in {continent}",
            "content_text":[f"Here is a list of all items of {filter} '{filter_string}' in {continent} ({len(content)} in total):"],
            "content": content
        }
    

class Search_Items(TemplateView):
    template_name = "warehouse.html"
    def get_context_data(self, location):
        links, style, continent = menu_links_style(("search", location))
        return {
            "reg": get_reg_from_request(self.request),
            "style":style,
            "links": links,
            "location":location,
            "title":f"{'A' if location == 'EU' else 'B' if location == 'USA' else 'C' if location == 'ASIA' else 'D'}-Warehouse {location}",
            "header_text": "Search an Item",
            "content_text":[f"Here you can search an Item in {continent}:"],
            "search_item": True,
            "search_prompt": "What are you looking for?"
        }

class Search_Items_Result(TemplateView):
    template_name = "warehouse.html"
    def get_context_data(self, location, search_term):
        links, style, continent = menu_links_style(("filter_items", location))        
        # Split the search term into individual words
        search_words = search_term.split()
        # Create a Q object to build the query dynamically
        query = Q(shipped = False)
        # Iterate over each word and add a condition to the query
        for word in search_words:
            query &= Q(category__icontains=word) | Q(state__icontains=word)# now query based on location
        if location == "ALL":
            content_links = (
                Item.objects
                .filter(query)
                .values('category', 'state')
                .annotate(count=Count('id'))
                .distinct()
            )
        else:
            wh = 1 if location == "EU" else 2 if location == "USA" else 3 if location == "ASIA" else 4
            content_links = (
                Item.objects
                .filter(query, warehouse=wh)
                .values('category', 'state')
                .annotate(count=Count('id'))
                .distinct()
            )
        content_text = f"'{search_term}' didn't match any result for items in {continent}" \
            if not len(content_links) else f"Your search for '{search_term}' in {continent} has {len(content_links)} matches:"
        return {
            "reg": get_reg_from_request(self.request),
            "style":style,
            "links": links,
            "location":location,
            "title":f"{'A' if location == 'EU' else 'B' if location == 'USA' else 'C' if location == 'ASIA' else 'D'}-Warehouse {location}",
            "header_text": f"Search results for '{search_term}'",
            "content_text":[content_text],
            "filtered_by": "name",
            "content_links": content_links,
            "search_item": True,
            "search_prompt": "Not what are you looking for?"
        }
    
class WorkingHoursView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "employees.html"
    def get_context_data(self):
        links, style, continent = menu_links_style(("filter_items", "location"))
        # Query all EmployeeWorkingHours records and order them by employee and week_day
        working_hours = EmployeeWorkingHours.objects.select_related('employee').order_by('employee__id', 'week_day')

        # Create a dictionary to store working hours grouped by employee
        employee_working_hours = {}
        for hour in working_hours:
            employee = hour.employee
            if employee not in employee_working_hours:
                employee_working_hours[employee] = []
            employee_working_hours[employee].append(hour)
        return {
            "reg": get_reg_from_request(self.request),
            "style":style,
            "links": links,
            "title":"working Hours",
            "header_text": "All Working Hours",
            "content_text":[f"Here is a list of all employees in {continent}:"],
            'employee_working_hours': employee_working_hours
        }