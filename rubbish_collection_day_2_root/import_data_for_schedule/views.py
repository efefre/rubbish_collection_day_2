from django.contrib import messages
from django.shortcuts import render, reverse
from .forms import (
    UploadStreetsForm,
    AddStreetsToCityForm,
    AddAddressToRubbishDistrictForm,
    AddDatesToRubbishDistrictForm,
)
from .utils import get_streets_names
from city_detail.models import Street, City, Address
from schedule.models import RubbishDistrict
from schedule.models import RubbishDistrict, Date
from django.views.generic import TemplateView, FormView
from datetime import datetime

from .replace_streets import wolomin_streets


# Create your views here.
class ImportDataView(TemplateView):
    template_name = "import_data_for_schedule/import_data.html"


class LoadDistrictOptionsView(TemplateView):
    template_name = "import_data_for_schedule/district_dropdown_list_options.html"

    def get_context_data(self, **kwargs):
        city_pk = self.request.GET.get("city")
        rubbish_type_pk = self.request.GET.get("rubbishType")
        city = City.objects.get(pk=city_pk)
        districts = RubbishDistrict.objects.filter(city_type=city.city_type, rubbish_type=rubbish_type_pk).order_by("rubbish_type", "name")
        context = super().get_context_data(**kwargs)
        context["districts"] = districts
        return context

class LoadDistrictOptionsCityTypeView(TemplateView):
    template_name = "import_data_for_schedule/district_dropdown_list_option_by_city_type.html"

    def get_context_data(self, **kwargs):
        city_type = self.request.GET.get("cityType")
        rubbish_type_pk = self.request.GET.get("rubbishType")
        districts = RubbishDistrict.objects.filter(city_type=city_type, rubbish_type=rubbish_type_pk).order_by("rubbish_type", "name")
        context = super().get_context_data(**kwargs)
        context["districts"] = districts
        return context


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

            if wolomin_streets.get(street):
                street = wolomin_streets.get(street)
            elif '-go ' in street:
                street = street.replace('-go ',' ')
            elif '- go ' in street:
                street = street.replace('- go ', ' ')

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


class AddAddressToRubbishDistrictView(FormView):
    form_class = AddAddressToRubbishDistrictForm
    template_name = "import_data_for_schedule/add_address_to_district.html"

    def get_success_url(self):
        return reverse("import_data_for_schedule:add-address-to-district")

    def form_valid(self, form):
        streets = (form.cleaned_data["streets"]).replace(", ", ",").split(",")
        city = form.cleaned_data["city"]
        rubbish_district = form.cleaned_data["rubbish_district"]
        context = self.get_context_data()

        rubbish_district_id = RubbishDistrict.objects.get(pk=rubbish_district.pk)

        add_rubbish_district = None
        address_does_not_exist = []
        for street in streets:
            street_id = Street.objects.filter(name__startswith=street.strip())
            for str_id in street_id:
                try:
                    address_id = Address.objects.get(city=city, street=str_id)
                except Address.DoesNotExist:
                    address_does_not_exist.append(str_id.name)
                else:
                    address_id.rubbish_district.add(rubbish_district_id)
                    add_rubbish_district = True

        if address_does_not_exist:
            message_error = messages.error(
                self.request,
                f'Taki adres nie istnieje. {city}: {", ".join(address_does_not_exist)}',
            )
            context["message_error"] = message_error
        if add_rubbish_district:
            message_success = messages.success(
                self.request, f"Dodano {rubbish_district} do wybranych adresów."
            )
            context["message_success"] = message_success
        return super().form_valid(form)


class AddDatesToRubbishDistrictView(FormView):
    form_class = AddDatesToRubbishDistrictForm
    template_name = "import_data_for_schedule/add_dates_to_district.html"

    def get_success_url(self):
        return reverse("import_data_for_schedule:add-dates-to-district")

    def form_valid(self, form):
        dates = (form.cleaned_data["dates"]).split("\n")
        rubbish_district = form.cleaned_data["rubbish_district"]
        rubbish_district_id = RubbishDistrict.objects.get(pk=rubbish_district.pk)
        context = self.get_context_data()

        add_date = None
        date_does_not_exist = []
        for date in dates:
            converted_date = datetime.strptime(date.strip(), "%d.%m.%Y").date()
            try:
                date_id = Date.objects.get(date=converted_date)
            except Date.DoesNotExist:
                date_does_not_exist.append(date)
            else:
                rubbish_district_id.date.add(date_id)
                add_date = True

        if date_does_not_exist:
            message_error = messages.error(
                self.request,
                f'Takie daty nie istnieją w bazie: {", ".join(date_does_not_exist)}',
            )
            context["message_error"] = message_error
        if add_date:
            message_success = messages.success(
                self.request, f"Dodano daty do: {rubbish_district}."
            )
            context["message_success"] = message_success

        return super().form_valid(form)
