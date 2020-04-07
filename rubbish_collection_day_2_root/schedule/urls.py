from django.urls import path
from .views import HomeView, LoadStreetView, CalendarView

app_name = "schedule"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('ajax/load-streets/', LoadStreetView.as_view(), 
         name='ajax_load_streets'),
    path("calendar/", CalendarView.as_view(), name='calendar')
    ]
