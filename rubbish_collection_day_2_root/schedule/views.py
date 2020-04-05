from django.shortcuts import render
from django.views.generic import FormView
from .forms import ChooseAddress


# Create your views here.
class HomeView(FormView):
    form_class = ChooseAddress
    template_name = "schedule/home.html"
