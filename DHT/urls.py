from django.urls import path
from . import views
from . import api
from django.contrib.auth import views as auth_views
from django.urls import path


urlpatterns = [
    path("api",api.Dlist,name='json'),
    path("api/post",api.Dlist,name='json'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('dashboard/',views.table,name='dashboard'),
    path('Charts/',views.graphs,name='Charts'),
    path('chart-data/', views.chart_data, name='chart-data'),
    path('manuel_post/',views.manuel_post,name='manuel_post'),
    path('chart-data-jour/',views.chart_data_jour,name='chart_data_jour'),
    path('chart-data-semaine/',views.chart_data_semaine,name='chart_data_semaine'),
    path('chart-data-mois/',views.chart_data_mois,name='chart_data_mois'),
    path('', views.home, name='home'),
    path('json/', views.post_temperature_humidity, name='json'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('user-login/', views.user_login, name='user_login'),
    path('incidents/', views.incidents, name='incidents'),
    path('administration/', views.administration, name='administration'),
    path('clear-data/', views.clear_data, name='clear_data'),
    path('Adminincidents/', views.adminincidents, name='Adminincidents'),

]