from django.urls import path, re_path
from . import views


app_name = "web_pages"

urlpatterns = [
    path('<slug:slug>/', views.web_page_view, name="page_view")
]
