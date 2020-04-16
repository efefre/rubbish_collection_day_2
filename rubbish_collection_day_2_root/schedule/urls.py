from django.urls import path
from .views import HomeView, LoadStreetView, CalendarView, DynamicCssNameView

app_name = "schedule"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('ajax/load-streets/', LoadStreetView.as_view(), 
         name='ajax_load_streets'),
    path("calendar/", CalendarView.as_view(), name='calendar'),
    path('calendar/mark-rubbish.css', DynamicCssNameView.as_view(), name='mark-rubbish-css')
    ]
