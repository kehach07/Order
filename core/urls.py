from django.urls import path
from .views import AddressListCreateAPI, AddressUpdateAPI, DashboardAPI, OrderListCreateAPI, ProductListCreateAPI, SignupAPI, SigninAPI, ProfileDetailAPI

urlpatterns = [
    path("signup/", SignupAPI.as_view(), name="signup"),
    path("signin/", SigninAPI.as_view(), name="signin"),
    path("profile/", ProfileDetailAPI.as_view(), name="profile"),

    path("products/", ProductListCreateAPI.as_view(), name="products"),

    path("addresses/", AddressListCreateAPI.as_view(), name="addresses"),
    path("addresses/<int:pk>/", AddressUpdateAPI.as_view(), name="address-update"),

    path("orders/", OrderListCreateAPI.as_view(), name="orders"),
    
    path("dashboard/", DashboardAPI.as_view(), name="dashboard"),
]

