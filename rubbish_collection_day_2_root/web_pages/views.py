from django.shortcuts import render, get_object_or_404
from .models import WebPage


# Create your views here.
def web_page_view(request, slug):
    page = get_object_or_404(WebPage, slug=slug, status='published')
    return render(request, 'web_pages/page_view.html',
                            {'page': page})

