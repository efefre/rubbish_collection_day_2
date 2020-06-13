from django.urls import path
from . import views

app_name = "import_data_for_schedule"


urlpatterns = [
    path("streets/", views.import_streets, name="import-streets"),
]
