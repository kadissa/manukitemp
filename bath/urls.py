from django.urls import path
from . import views

appname = 'bath'

urlpatterns = [
    path('success/', views.success, name='success'),
    path('create_appointment/', views.appointment_create,
         name='appointment_create'),
    path('<int:pk>', views.items_view, name='service'),
    path('temp', views.temp, name='temp'),
    path('finish', views.get_finish, name='finish'),

]
