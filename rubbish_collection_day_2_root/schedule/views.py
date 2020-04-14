from django.views.generic import FormView, TemplateView
from .forms import ChooseAddressForm
from city_detail.models import Address
from schedule.models import RubbishDistrict
from .utils import days_for_calendar
from collections import defaultdict


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
        address = Address.objects.select_related("city", "street").get(
            city__name=city_name, street__name=street_name
        )
        rubbish_districts = RubbishDistrict.objects.select_related("rubbish_type").prefetch_related('date').filter(addresses=address)
        schedule_dates_for_address = defaultdict(list)

        for district in rubbish_districts:
            for date in district.date.all():
                schedule_dates_for_address[date.date].append(district)

        context["calendar"] = days_for_calendar(2020)
        context["days_names_list"] = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        context["address"] = address
        context["schedule_dates_for_address"] = dict(schedule_dates_for_address)

        return context
