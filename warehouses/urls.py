from django.urls import path
from .views import (
    Index,
    Warehouse,
    About,
    Products,
    List_Filtered,
    List_Items_Filtered,
)

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("about", About.as_view(), name="about"),
    path("<str:location>", Warehouse.as_view(), name="warehouse"),
    path("<str:location>/products", Products.as_view(), name="products"), #list items per warehouse
    path("<str:location>/<str:filter>/<str:filter_string>", List_Items_Filtered.as_view(), name="category_items"), #list items of category per warehouse
    path("<str:location>/<str:filter>", List_Filtered.as_view(), name="categories"), #list categories per warehouse
]