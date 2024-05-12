from django.urls import path
from . import views

appname = 'bath'

urlpatterns = [
    path('success/', views.success, name='success'),
    path('create_appointment/', views.appointment_create,
         name='appointment_create'),
    path('<int:pk>', views.items_view, name='service'),
    path('temp', views.get_day, name='temp'),
    path('finish', views.get_user_and_services, name='finish'),
    path('date/', views.get_date, name='date'),
    path('time/<str:day>/', views.get_time, name='time'),
    path('user/', views.get_user_and_date, name='user')

]
