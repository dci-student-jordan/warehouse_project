# warehouses.views.py

from typing import Any
from django.http import HttpResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic.base import TemplateView
from .models import Item
from django.db.models import Q

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
        if "menu" in link.keys():
            link["menu"] = [l for l in link["menu"] if not l["link"] == exclude]
        if link["link"] == exclude:
            menu = link["menu"][1:]
            link = link["menu"][0]
            link["menu"] = menu
        return link
    links = [un_menu(link) for link in links]
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
        if location == "ALL":
            content = Item.objects.all()
        else:
            wh = 1 if location == "EU" else 2 if location == "USA" else 3 if location == "ASIA" else 4
            content = Item.objects.filter(warehouse=wh)
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

class List_Filtered(TemplateView):
    template_name = "warehouse.html"
    def get_context_data(self, location, filter):
        links, style, continent = menu_links_style(("filter", location))
        if location == "ALL":
            content_links = Item.objects.all().values(filter).distinct()
        else:
            wh = 1 if location == "EU" else 2 if location == "USA" else 3 if location == "ASIA" else 4
            content_links = Item.objects.filter(warehouse=wh).values(filter).distinct()
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
        links, style, continent = menu_links_style(("filter_items", location))
        args = {filter:filter_string}
        if location == "ALL":
            content = Item.objects.filter(**args)
        else:
            wh = 1 if location == "EU" else 2 if location == "USA" else 3 if location == "ASIA" else 4
            content = Item.objects.filter(warehouse=wh, **args)
        return {
            "reg": get_reg_from_request(self.request),
            "style":style,
            "links": links,
            "location":location,
            "title":f"{'A' if location == 'EU' else 'B' if location == 'USA' else 'C' if location == 'ASIA' else 'D'}-Warehouse {location}",
            "header_text":f"Items of {filter} '{filter_string}' in {content}",
            "content_text":[f"Here is a list of all items of {filter} '{filter_string}' in {continent} ({len(content)} in total):"],
            "content": content
        }
    

class Search_Items(TemplateView):
    template_name = "warehouse.html"
    def get_context_data(self, location):
        links, style, continent = menu_links_style(("filter_items", location))
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
        query = Q()
        # Iterate over each word and add a condition to the query
        for word in search_words:
            query |= Q(category__icontains=word) | Q(state__icontains=word)
        # now query based on location
        if location == "ALL":
            content_links = Item.objects.filter(query).distinct()
        else:
            wh = 1 if location == "EU" else 2 if location == "USA" else 3 if location == "ASIA" else 4
            content_links = Item.objects.filter(query, warehouse=wh).distinct()
        content_text = f"'{search_term}' didn't match any result for items in {continent}" \
            if not len(content_links) else f"Your search for '{search_term}' in {continent} has {len(content_links)} matches:"
        return {
            "reg": get_reg_from_request(self.request),
            "style":style,
            "links": links,
            "location":location,
            "title":f"{'A' if location == 'EU' else 'B' if location == 'USA' else 'C' if location == 'ASIA' else 'D'}-Warehouse {location}",
            "header_text": f"Search results for '{search_term}'",
            "content_text":[content_text, "", "Search something else here:"],
            "filtered_by": "name",
            "content_links": content_links,
            "search_item": True,
            "search_prompt": "Not what are you looking for?"
        }