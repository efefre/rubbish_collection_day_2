from django.urls import path
from .views import HomeView, LoadStreetView

app_name = "schedule"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('ajax/load-streets/', LoadStreetView.as_view(), 
         name='ajax_load_streets'),
    ]
