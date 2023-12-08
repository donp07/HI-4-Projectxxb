from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import GlucoseReading
from django.utils.dateparse import parse_datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.utils.dateparse import parse_datetime
from .forms import RegisterForm
from .models import GlucoseReading
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import matplotlib.pyplot as plt
from django.http import HttpResponse
from .models import GlucoseReading
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

@login_required
def glucose_reading_list(request):
    if request.method == 'GET':
        readings = GlucoseReading.objects.filter(user=request.user)
        return render(request, 'base/glucose_readings_list.html', {'readings': readings})


    elif request.method == 'POST':
        reading = request.POST.get('reading')
        date_time_str = request.POST.get('date_time')

        # Parse the datetime string to a datetime object
        date_time = parse_datetime(date_time_str)

        if reading and date_time:
            GlucoseReading.objects.create(
                user=request.user,
                reading=reading,
                date_time=date_time
            )
        return redirect('glucose_reading_list')

@login_required
def glucose_reading_graph(request):
    readings = GlucoseReading.objects.filter(user=request.user).order_by('date_time')

    # Prepare data
    dates = [reading.date_time.strftime("%Y-%m-%d %H:%M") for reading in readings]
    values = [reading.reading for reading in readings]

    # Create a Matplotlib figure
    fig, ax = plt.subplots()
    ax.plot(dates, values)
    ax.set(title='Glucose Readings', xlabel='Date', ylabel='Reading')

    # Rotate date labels
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Create a canvas and output as HTTP response
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    plt.close(fig)

    return response

def login_view(request):
    return auth_views.LoginView.as_view(template_name='base/login.html')(request)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # You can also log the user in and redirect them to another page
            return redirect('login')  # Redirect to login page after registration
    else:
        form = RegisterForm()
    return render(request, 'base/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout