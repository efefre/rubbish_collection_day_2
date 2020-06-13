from django.contrib import messages
from django.shortcuts import render
from .forms import UploadStreetsForm


# Create your views here.
def import_streets(request):
    if request.method == 'POST':
        form = UploadStreetsForm(request.POST, request.FILES)
        if form.is_valid():
            message =  messages.success(request, 'Plik został dodany')
            render(request, 'import_data_for_schedule/upload_streets.html', {'form': form, 'message': message})
    else:
        form = UploadStreetsForm()
    return render(request, 'import_data_for_schedule/upload_streets.html', {'form': form})
