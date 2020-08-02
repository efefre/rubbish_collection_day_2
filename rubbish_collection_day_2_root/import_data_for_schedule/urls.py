from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = "import_data_for_schedule"


urlpatterns = [
    path("", login_required(views.ImportDataView.as_view()), name="import-data"),
    path("streets/", login_required(views.import_streets), name="import-streets"),
    path(
        "add-streets-to-city/",
        login_required(views.AddStreetToCityView.as_view()),
        name="add-streets-to-city",
    ),
    path(
        "add-address-to-district/",
        login_required(views.AddAddressToRubbishDistrictView.as_view()),
        name="add-address-to-district",
    ),
    path(
        "ajax/load-districts-options/",
        login_required(views.LoadDistrictOptionsView.as_view()),
        name="ajax_load_districts_otpions"),
    path(
        "ajax/load-districts-options-by-city-type/",
        login_required(views.LoadDistrictOptionsCityTypeView.as_view()),
        name="ajax_load_districts_otpions_city_type"),
    path(
        "add-dates-to-district/",
        login_required(views.AddDatesToRubbishDistrictView.as_view()),
        name="add-dates-to-district",
    ),
]
