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
        context["calendar"] = days_for_calendar(2020)
        return context
