import telepot
from .models import Dht11  # Assurez-vous d'importer le modèle Dht11
from django.utils import timezone
import csv
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import timedelta
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import logout
from .models import UserComment


def home(request):
    return render(request, 'login.html')

from django.db.models import Max, Min

@login_required
def table(request):
    """
    View for the dashboard. Fetches the latest temperature and humidity data,
    along with the maximum and minimum historical values.
    """
    derniere_ligne = Dht11.objects.last()  # Fetch the latest record
    if not derniere_ligne:
        valeurs = {
            'date': 'No data available',
            'temp': 'N/A',
            'hum': 'N/A',
            'max_temp': 'N/A',
            'min_temp': 'N/A',
            'max_hum': 'N/A',
            'min_hum': 'N/A',
        }
    else:
        # Calculate the time difference
        derniere_date = derniere_ligne.dt
        delta_temps = timezone.now() - derniere_date
        difference_minutes = delta_temps.seconds // 60
        temps_ecoule = f'il y a {difference_minutes} min'
        if difference_minutes > 60:
            temps_ecoule = f'il y a {difference_minutes // 60}h {difference_minutes % 60}min'

        # Fetch max and min temperature and humidity
        max_temp = Dht11.objects.aggregate(Max('temp'))['temp__max']
        min_temp = Dht11.objects.aggregate(Min('temp'))['temp__min']
        max_hum = Dht11.objects.aggregate(Max('hum'))['hum__max']
        min_hum = Dht11.objects.aggregate(Min('hum'))['hum__min']

        valeurs = {
            'date': temps_ecoule,
            'temp': derniere_ligne.temp,
            'hum': derniere_ligne.hum,
            'max_temp': max_temp,
            'min_temp': min_temp,
            'max_hum': max_hum,
            'min_hum': min_hum,
        }

    return render(request, 'dashboard.html', {'valeurs': valeurs})

def download_csv(request):
    model_values = Dht11.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dht.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response
#pour afficher navbar de template
def index_view(request):
    return render(request, 'index.html')

#pour afficher les graphes
def graphs(request):
    return render(request, 'Charts.html')
def manuel_post(request):
    return render(request, 'manuel_post.html')
# récupérer toutes les valeur de température et humidity sous forme un #fichier json
def chart_data(request):
    dht = Dht11.objects.all()

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)


def chart_data_jour(request):
    # Récupérer les données des dernières 24 heures
    now = timezone.now()
    last_24_hours = now - datetime.timedelta(hours=24)
    data = Dht11.objects.filter(dt__gte=last_24_hours)

    temps = [entry.dt.strftime('%H:%M') for entry in data]
    temperature = [entry.temp for entry in data]
    humidity = [entry.hum for entry in data]

    return JsonResponse({'temps': temps, 'temperature': temperature, 'humidity': humidity})

def chart_data_semaine(request):
    # Récupérer les données de la dernière semaine
    now = timezone.now()
    last_week = now - datetime.timedelta(days=7)
    data = Dht11.objects.filter(dt__gte=last_week)

    temps = [entry.dt.strftime('%b %d') for entry in data]
    temperature = [entry.temp for entry in data]
    humidity = [entry.hum for entry in data]

    return JsonResponse({'temps': temps, 'temperature': temperature, 'humidity': humidity})

def chart_data_mois(request):
    # Récupérer les données du dernier mois
    now = timezone.now()
    last_month = now - datetime.timedelta(days=30)
    data = Dht11.objects.filter(dt__gte=last_month)

    temps = [entry.dt.strftime('%b') for entry in data]
    temperature = [entry.temp for entry in data]
    humidity = [entry.hum for entry in data]

    return JsonResponse({'temps': temps, 'temperature': temperature, 'humidity': humidity})



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def sendtele():
    token = '6662023260:AAG4z48OO9gL8A6szdxg0SOma5hv9gIII1E'
    rece_id = 1242839034
    bot = telepot.Bot(token)
    bot.sendMessage(rece_id, 'la température depasse la normale')
    print(bot.sendMessage(rece_id, 'OK.'))


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Dht11

@csrf_exempt
def post_temperature_humidity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Charger les données JSON
            temp = data.get('temp')
            hum = data.get('hum')

            # Vérifiez que les données nécessaires sont présentes
            if temp is not None and hum is not None:
                # Sauvegarder les données dans la base de données
                new_entry = Dht11(temp=temp, hum=hum)
                new_entry.save()
                return JsonResponse({'status': 'success', 'message': 'Data saved successfully'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Missing temp or hum in request'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

from django.contrib.auth.models import Group

# Create groups for normal users and administrators
normal_user_group, created = Group.objects.get_or_create(name='normal_user')
admin_group, created = Group.objects.get_or_create(name='administrator')
from django.contrib.auth.models import User

# Assign user to the 'administrator' group
user = User.objects.get(username='example_user')
admin_group = Group.objects.get(name='administrator')
user.groups.add(admin_group)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
@csrf_exempt
def login_view(request):
    """
    Handles login for users and admins.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        action = request.POST.get('action')  # Determine if user clicked 'User' or 'Admin'

        user = authenticate(request, username=username, password=password)
        if user:
            if action == 'admin' and user.groups.filter(name='administrator').exists():
                login(request, user)
                return redirect('dashboard')  # Redirect to admin dashboard
            elif action == 'user':
                login(request, user)
                return redirect('dashboard')  # Redirect to user dashboard
            else:
                messages.error(request, "Unauthorized access for this role!")
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, 'login.html')

from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.groups.filter(name='administrator').exists()

from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administrator').exists())
def admin_dashboard(request):
    # Dashboard logic here
    return render(request, 'admin_dashboard.html')

@login_required
def admin_dashboard(request):
    """
    Admin dashboard view.
    """
    return render(request, 'admin_dashboard.html')  # Replace with actual admin dashboard template

@login_required
def user_dashboard(request):
    """
    Normal user dashboard view.
    """
    return render(request, 'dashboard.html')  # Replace with actual user dashboard template

@csrf_exempt
def admin_login(request):
    """
    Automatically logs in as an admin.
    """
    # Create or fetch a default admin user
    admin_user, created = User.objects.get_or_create(username="admin_user")
    if created:
        admin_user.set_unusable_password()  # No password required
        admin_user.save()
        # Add the user to the 'administrator' group
        admin_group, _ = Group.objects.get_or_create(name="administrator")
        admin_group.user_set.add(admin_user)

    login(request, admin_user)
    return redirect('dashboard')  # Replace with the actual admin dashboard URL

@csrf_exempt
def user_login(request):
    """
    Automatically logs in as a normal user.
    """
    # Create or fetch a default normal user
    normal_user, created = User.objects.get_or_create(username="normal_user")
    if created:
        normal_user.set_unusable_password()  # No password required
        normal_user.save()
        # Add the user to the 'normal_user' group
        user_group, _ = Group.objects.get_or_create(name="normal_user")
        user_group.user_set.add(normal_user)

    login(request, normal_user)
    return redirect('dashboard')  # Replace with the actual user dashboard URL


from django.contrib.auth.models import User, Group
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not password1 or not password2:
            messages.error(request, "All fields are required.")
        elif password1 != password2:
            messages.error(request, "Passwords do not match!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
        else:
            # Create the user
            user = User.objects.create_user(username=username, password=password1)
            # Add the user to the 'normal_user' group by default
            group, _ = Group.objects.get_or_create(name='normal_user')
            user.groups.add(group)

            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login_view')

    return render(request, 'register.html')

from .models import Dht11, UserComment  # Ensure UserComment is imported
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def incidents(request):
    """
    Page to display incidents and allow users to comment.
    """
    # Fetch the most recent data entry (regardless of temperature)
    latest_data = Dht11.objects.last()

    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if latest_data and comment_text:
            # Create a new UserComment record
            UserComment.objects.create(
                user=request.user,
                temperature=latest_data.temp,
                comment=comment_text
            )
            return redirect('incidents')  # Refresh the page after submission

    return render(request, 'incidents.html', {'latest_data': latest_data})

from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.groups.filter(name='administrator').exists()

@login_required
@user_passes_test(is_admin)
def administration(request):
    """
    Page that displays all comments submitted via the incidents page.
    Only accessible to admin users.
    """
    # Order the comments by timestamp (most recent first)
    comments = UserComment.objects.all().order_by('-timestamp')
    return render(request, 'administration.html', {'comments': comments})

from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Dht11

def clear_data(request):
    """
    Clears all records in the Dht11 table.
    """
    if request.method == "POST":
        Dht11.objects.all().delete()
        return HttpResponse("All data cleared successfully.")
    return redirect('dashboard')  # Redirect to the dashboard after clearing

def adminincidents(request):
    return render(request, 'Adminincidents.html')