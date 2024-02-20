from warehouses.views import menu_links_style
from django.template import RequestContext

def custom_context(request):
    context = {}
    
    # Check if the request path matches the auth urls
    if request.path.startswith('/user/auth'):
        location = request.GET.get('location', "")
        links, style, continent = menu_links_style(("filter", location))
        context["style"] = style
        context["links"] = links
        context["location"] = location
        context["title"] = f"{'A' if location == 'EU' else 'B' if location == 'USA' else 'C' if location == 'ASIA' else 'D'}-Warehouse {location}"

    return context

