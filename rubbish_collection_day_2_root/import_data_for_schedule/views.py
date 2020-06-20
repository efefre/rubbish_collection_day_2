from django.contrib import messages
from django.shortcuts import render, reverse
from .forms import UploadStreetsForm, AddStreetsToCityForm
from .utils import get_streets_names
from city_detail.models import Street, City, Address
from django.views.generic.edit import FormView


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


class AddStreetToCityView(FormView):
    form_class = AddStreetsToCityForm
    template_name = "import_data_for_schedule/add_streets.html"

    def get_success_url(self):
        return reverse("import_data_for_schedule:add-streets-to-city")

    def form_valid(self, form):
        streets = (form.cleaned_data["streets"]).replace(", ", ",").split(",")
        city = form.cleaned_data["city"]
        context = self.get_context_data()

        new_streets = []
        add_address = None
        street_err = []
        for street in streets:
            street = street.replace("\r\n", " ")
            city_id = City.objects.get(name=city)

            street_id = Street.objects.get_or_create(name=street.strip())
            if street_id[1]:
                new_streets.append(street)
            else:
                address = Address.objects.get_or_create(
                    city=city_id, street=street_id[0]
                )
                if address[1]:
                    add_address = True
                else:
                    street_err.append(street)

        if new_streets:
            message_warnings = messages.warning(
                self.request, f'Dodano nowe ulice: {", ".join(new_streets)}'
            )
            context["message_warnings"] = message_warnings

        if add_address:
            message_success = messages.success(
                self.request, f"Dodano nowe adresy w miejscowości {city}"
            )
            context["message_success"] = message_success

        if street_err:
            message_error = messages.error(
                self.request,
                f'Taki adres już istnieje. {city}: {", ".join(street_err)}',
            )
            context["message_error"] = message_error

        return super().form_valid(form)
