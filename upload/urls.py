from django.urls import path
from . import views

urlpatterns = [
    path('', views.display, name='display'),
    path('excel_file/', views.excel_file, name='excel_file'),
    path('approved/', views.approved, name='approved'),
]