from warehouses.views import menu_links_style
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse

def custom_context(request):
    context = {}
    
    # Check if the request path matches the auth urls
    if request.path.startswith('/user/auth') or \
            request.path.startswith('/user/login_required') or \
            request.path.startswith('/thanks') or \
            request.path.startswith('/not_found'):
        # print("PROCESSED")
        location = request.GET.get('location', "")
        links, style, continent = menu_links_style(("filter", location))
        context["style"] = style
        context["links"] = links
        context["location"] = location
        context["title"] = f"{'A' if location == 'EU' else 'B' if location == 'USA' else 'C' if location == 'ASIA' else 'D'}-Warehouse {location}"
    # elif (request.path.split("/")[0] not in ["about", "ALL", "EU", "USA", "ASIA", "INDIA"]):
    #     redir = reverse_lazy("not_found")
    #     print("WTF:", redir)
    #     return redirect("not_found/")

    return context

