from django.views.generic import FormView, TemplateView
from .forms import ChooseAddress
from city_detail.models import Address


# Create your views here.
class HomeView(FormView):
    form_class = ChooseAddress
    template_name = "schedule/home.html"


# Street - dropdown list option
class LoadStreetView(TemplateView):
    template_name = "schedule/street_dropdown_list_options.html"

    def get_context_data(self, **kwargs):
        city_id = self.request.GET.get('city')
        streets = Address.objects.filter(city__pk=city_id).order_by('street')
        context = super().get_context_data(**kwargs)
        context["streets"] = streets
        return context
