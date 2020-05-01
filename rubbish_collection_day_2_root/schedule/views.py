from django.views.generic import FormView, TemplateView
from .forms import ChooseAddressForm
from city_detail.models import Address
from schedule.models import RubbishDistrict, RubbishType
from .utils import days_for_calendar
from collections import defaultdict
from itertools import combinations
from schedule.models import ScheduleConfiguration


config = ScheduleConfiguration.get_solo()
YEAR = int(config.year)
TECH_BREAK = config.maintenance_mode


class HomeView(FormView):
    form_class = ChooseAddressForm
    template_name = "schedule/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["technical_break"] = TECH_BREAK
        return context


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
        rubbish_districts = (
            RubbishDistrict.objects.select_related("rubbish_type")
            .prefetch_related("date")
            .filter(addresses=address)
        )
        schedule_dates_for_address = defaultdict(list)

        for district in rubbish_districts:
            for date in district.date.all():
                schedule_dates_for_address[date.date].append(district)

        context["form"] = ChooseAddressForm
        context["year"] = YEAR
        context["calendar"] = days_for_calendar(YEAR)
        context["days_names_list"] = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        context["address"] = address
        context["schedule_dates_for_address"] = dict(schedule_dates_for_address)
        context["technical_break"] = TECH_BREAK
        return context


class DynamicCssNameView(TemplateView):
    template_name = "schedule/css/mark-rubbish.css"
    content_type = "text/css"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rubbish_type = RubbishType.objects.all()

        all_css_combination = []
        rubbish_type_css = []
        for rubbish in rubbish_type:
            rubbish_type_css.append(rubbish.css_name)

        i = 1
        while i <= len(rubbish_type_css):
            rub_combinations = combinations(rubbish_type_css, i)
            for comb in rub_combinations:
                all_css_combination.append(sorted(list(comb)))

            i += 1
        css_names = ["-".join(_) for _ in all_css_combination]

        context["rubbish_type_css"] = css_names

        return context


class GenerateSvgView(TemplateView):
    template_name = "schedule/svg/generate-svg.svg"
    content_type = "image/svg+xml"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_name = kwargs.get("class_name")

        rubbish_types_details = RubbishType.objects.all()
        rubbish_colors = {}

        for rubbish in rubbish_types_details:
            rubbish_colors[rubbish.css_name] = rubbish.mark_color

        rubbish_types_from_url = (class_name.replace("-rubbish", "")).split("-")

        color_svg = []

        for rubbish in rubbish_types_from_url:
            color_svg.append(rubbish_colors.get(rubbish))

        context["color_svg"] = color_svg
        return context
