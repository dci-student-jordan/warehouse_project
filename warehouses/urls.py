from django.urls import path
from .views import (
    NotFound,
    Index,
    Warehouse,
    About,
    Products,
    ProductDetailView,
    List_Filtered,
    List_Items_Filtered,
    Search_Items,
    Search_Items_Result,
    WorkingHoursView,
    OrderView,
    Thanks
)

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("about/", About.as_view(), name="about"),
    path("not_found/", NotFound.as_view(), name="not_found"),
    path("thanks/<str:action>", Thanks.as_view(), name="thanks"),
    path("<str:location>/", Warehouse.as_view(), name="warehouse"),
    path("<str:location>/products/", Products.as_view(), name="products"), # list items per warehouse
    path("<str:location>/order/<str:state>/<str:category>/", OrderView.as_view(), name="order"),
    path("stock/employees/", WorkingHoursView.as_view(), name="list_workinhours"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product_detail"), # edit items per warehouse
    path("<str:location>/search/", Search_Items.as_view(), name="search"), # search items per warehouse
    path("<str:location>/search/<str:search_term>", Search_Items_Result.as_view(), name="search_result"), # search items per warehouse
    path("<str:location>/<str:filter>/<str:filter_string>/", List_Items_Filtered.as_view(), name="filtered_items"), #items browser
    path("<str:location>/<str:filter>/", List_Filtered.as_view(), name="filtered"), #list categories/states per warehouse
]