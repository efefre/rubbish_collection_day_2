from django.urls import path
from .views import (
    HomeView,
    LoadStreetView,
    CalendarView,
    DynamicCssNameView,
    GenerateSvgView,
    ical,
)

app_name = "schedule"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "ajax/load-streets/",
        LoadStreetView.as_view(),
        name="ajax_load_streets"),
    path("calendar/", CalendarView.as_view(), name="calendar"),
    path(
        "calendar/mark-rubbish.css",
        DynamicCssNameView.as_view(),
        name="mark-rubbish-css",
    ),
    path(
        "calendar/svg/<str:class_name>.svg",
        GenerateSvgView.as_view(),
        name="svg"),
    path("calendar/ical/", ical, name="ical_calendar"),
]
