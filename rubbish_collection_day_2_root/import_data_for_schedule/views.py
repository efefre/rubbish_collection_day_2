from django.contrib import messages
from django.shortcuts import render
from .forms import UploadStreetsForm
from .utils import get_streets_names
from city_detail.models import Street


# Create your views here.
def import_streets(request):
    """Import streets from file and add to database"""

    if request.method == "POST":
        form = UploadStreetsForm(request.POST, request.FILES)
        if form.is_valid():
            streets = get_streets_names(request.FILES["file"])

            ex_streets = []
            add_street = None

            for street in streets:
                try:
                    Street.objects.get(name=street)
                except Street.DoesNotExist:
                    Street.objects.create(name=street)
                    add_street = True
                else:
                    ex_streets.append(street)

            if add_street:
                message_succes = messages.success(request, "Ulice zostały dodane.")

            if ex_streets:
                message_errors = messages.error(
                    request, f'Te ulice już istnieją: {", ".join(ex_streets)}'
                )

            if add_street and not ex_streets:
                render(
                    request,
                    "import_data_for_schedule/upload_streets.html",
                    {"form": form, "message_succes": message_succes},
                )
            elif add_street and ex_streets:
                render(
                    request,
                    "import_data_for_schedule/upload_streets.html",
                    {
                        "form": form,
                        "message_succes": message_succes,
                        "message_errors": message_errors,
                    },
                )
            else:
                render(
                    request,
                    "import_data_for_schedule/upload_streets.html",
                    {"form": form, "message_errors": message_errors},
                )
    else:
        form = UploadStreetsForm()
    return render(
        request, "import_data_for_schedule/upload_streets.html", {"form": form}
    )
