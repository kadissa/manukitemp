from django.urls import path
from . import views

appname = 'bath'

urlpatterns = [
    path('appointment/<str:day>/<int:user_id>', views.create_appointment,
         name='create_appointment'),
    path('confirm_items/<int:pk>', views.confirm_items,
         name='confirm_items'),
    path('service/<int:pk>', views.items_view, name='service'),
    path('finish/<int:appoint_id>', views.finish_view, name='finish'),
    path('time/<str:day>/<int:user_id>', views.get_time, name='time'),
    path('user/<int:user_id>', views.get_user_and_date, name='user'),
    path('error/', views.error, name='error'),

]
