from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="sales"),
    path('add-sale', views.add_sale, name="add-sale"),
]