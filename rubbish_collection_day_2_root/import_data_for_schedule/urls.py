from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = "import_data_for_schedule"


urlpatterns = [
    path("streets/", login_required(views.import_streets), name="import-streets"),
    path("add-streets-to-city/", login_required(views.AddStreetToCityView.as_view()), name="add-streets-to-city"),
]
