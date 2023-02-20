from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="sales"),
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer_detail/<uuid:customer_id>/', views.customer_detail, name='customer_detail'),
]