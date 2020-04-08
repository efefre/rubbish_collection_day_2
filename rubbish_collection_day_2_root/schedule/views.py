from django.views.generic import FormView, TemplateView
from .forms import ChooseAddressForm
from city_detail.models import Address
from .utils import days_for_calendar


class HomeView(FormView):
    form_class = ChooseAddressForm
    template_name = "schedule/home.html"


# Street - dropdown list option
class LoadStreetView(TemplateView):
    template_name = "schedule/street_dropdown_list_options.html"

    def get_context_data(self, **kwargs):
        city_name = self.request.GET.get("city")
        streets = Address.objects.filter(city__name=city_name).order_by("street")
        context = super().get_context_data(**kwargs)
        context["streets"] = streets
        return context


class CalendarView(TemplateView):
    template_name = "schedule/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city_name = self.request.GET.get("city")
        street_name = self.request.GET.get("street")
        address = Address.objects.get(city__name=city_name, street__name=street_name)

        temp_schedule_list = []
        schedule_for_address = {}
        for rubbish_district in address.rubbish_district.all():
            for date in rubbish_district.date.all():
                temp_schedule_list.append(
                    [date.date, rubbish_district.rubbish_type.name]
                )

        for i in temp_schedule_list:
            if schedule_for_address.get(i[0]):
                schedule_for_address[i[0]].append(i[1])
            else:
                schedule_for_address[i[0]] = [i[1]]

        context["calendar"] = days_for_calendar(2020)
        context["days_names_list"] = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        context["address"] = address
        context["schedule_for_address"] = schedule_for_address

        return context
