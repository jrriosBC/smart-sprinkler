from django.shortcuts import render
from sprinkler_operations.operations import Operations
from .forms import *

# Create your views here.
def dashboard(request):
    title = "Smart Sprinkler System"
    status = True
    form = PropertyForm(request.POST or None)

    context = {
        'title': title,
        'status': status,
        'form': form,
    }

    if request.POST and form.is_valid():
        operation = Operations()
        current_temp, forecast_high_temp, forecast_low_temp, recent_precip, forecast_precip = operation.get_weather()

        if form.is_valid():
            conditions = {
                "current_temp": current_temp,
                "forecast_high_temp": forecast_high_temp,
                "forecast_low_temp": forecast_low_temp,
                "recent_precip": recent_precip,
                "forecast_precip": forecast_precip,

            }

            context["conditions"]=conditions
            context['restrictions'] = operation.get_water_restrictions(
                form.cleaned_data['address_digit'],
                form.cleaned_data['property_type']
            )
            arduino_vals=operation.get_arduino_values()
            if not arduino_vals:
                arduino_vals = ['Not connected.'] * 2

            context['arduino_light']=arduino_vals[0]
            context['arduino_moisture']=arduino_vals[1]

            print conditions

    return render (request, 'dashboard.html', context)
