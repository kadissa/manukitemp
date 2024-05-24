from django.urls import path
from . import views

appname = 'bath'

urlpatterns = [
    path('cart/', views.cart_detail, name='cart'),
    path('products/', views.product_list, name='products'),
    path('appointment/<str:day>/<int:user_id>', views.create_appointment,
         name='create_appointment'),
    # path('confirm_items/<int:pk>', views.confirm_items,
    #      name='confirm_items'),
    # path('service/<int:pk>', views.items_view, name='service'),
    path('confirm_date_time/<int:appoint_id>', views.confirm_date_time, name='confirm_date_time'),
    path('time/<str:day>/<int:user_id>', views.get_time, name='time'),
    path('user/', views.get_customer_and_date, name='user'),
    path('error/', views.error, name='error'),

]
