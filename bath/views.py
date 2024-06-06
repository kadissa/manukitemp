import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django_htmx.http import HttpResponseClientRedirect

from .bath_price import get_price
from .cart import Cart
from .forms import CustomerForm
from .models import Customer, Appointment, Product, AppointmentItem

times = list()


def error(request):
    return render(request, 'error.html')


def add_items(request, pk):
    cart = Cart(request)
    products = Product.objects.all()
    appointment = Appointment.objects.get(pk=pk)
    for product in products:
        quantity = request.POST.get(f'{product}')
        cart.add_product(product=product,
                         appointment=appointment,
                         quantity=quantity)
    if request.method == 'POST':
        for item in cart.cart:
            AppointmentItem.objects.create(
                appointment=appointment,
                product=Product.objects.get(name=item),
                price=cart.cart[item]['price'],
                quantity=cart.cart[item]['quantity'],
            )
        items_price = AppointmentItem.objects.filter(
            appointment=appointment)
        appointment_items_price = sum(item.total_price for item in items_price)
        appointment.services_price = appointment_items_price
        appointment.save()
        return redirect('cart', pk=pk)
    context = {
        'products': products,
        'cart': cart,
        'appointment_id': pk
    }
    return render(request, 'products.html', context)


def cart_detail(request, pk):
    cart = Cart(request)
    appointment = get_object_or_404(Appointment, pk=pk)
    context = {
        'cart': cart,
        'appointment': appointment,
        'global_price': appointment.full_price
    }
    return render(request, 'cart_detail.html', context)


def confirm_date_time(request, appoint_id):
    appointment = get_object_or_404(Appointment, pk=appoint_id)
    context = {'appointment': appointment}
    return render(request, 'confirm_date_time.html', context)


def create_appointment(request, day, user_id):
    global times
    if not day or not times:
        return redirect('error')
    times_formatted = sorted(times)
    price = get_price(day, times)
    start_time = times_formatted[0][:5]
    end_time = times_formatted[-1][6:]
    customer = Customer.objects.get(pk=user_id)
    appointment, created = Appointment.objects.update_or_create(
        date=day, customer=customer, start_time=start_time,
        end_time=end_time, status='Не подтверждён', price=price,
        amount=len(times)
    )
    times = list()
    if created:
        return redirect('confirm_date_time', appointment.id)
    else:
        return redirect('error')


def get_customer_and_date(request):
    global times
    times = list()
    request_date = request.POST.get('date')
    customer_id = request.session.get('customer_id', 0)
    if Customer.objects.filter(id=customer_id).exists():
        customer = get_object_or_404(Customer,
                                     id=request.session['customer_id'])
        form = CustomerForm(request.POST or None, instance=customer)
    else:
        form = CustomerForm(request.POST or None)
    if form.is_valid():
        if not Customer.objects.filter(
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email']).exists():
            form.save()
        customer = Customer.objects.get(phone=form.cleaned_data['phone'],
                                        email=form.cleaned_data['email'])
        request.session['customer_id'] = customer.id
        return redirect('time', request_date, customer.id)
    today = datetime.date.today()
    min_day_value = today.isoformat()
    max_day_value = today + datetime.timedelta(days=60)
    context = {
        'min_day': min_day_value, 'max_day': max_day_value,
        'today': today.isoformat(), 'form': form, 'user_id': customer_id,
    }
    return render(request, 'user.html', context)


def get_time(request, day, user_id):
    global times
    all_time_dict = {'11': '11:00-12:00', '12': '12:00-13:00',
                     '13': '13:00-14:00',
                     '14': '14:00-15:00', '15': '15:00-16:00',
                     '16': '16:00-17:00',
                     '17': '17:00-18:00', '18': '18:00-19:00',
                     '19': '19:00-20:00',
                     '20': '20:00-21:00', '21': '21:00-22:00',
                     '22': '22:00-23:00'}
    today = datetime.date.today()
    request_time = request.POST.get('time')
    appointments = Appointment.objects.filter(
        date=datetime.date.fromisoformat(day))
    for appointment in appointments:  # get available slots for booking
        start = (appointment.start_time.isoformat('hours'))
        end = appointment.end_time.isoformat('hours')
        slots_to_remove = range(int(start) - 1, int(end) + 1)
        for slot in slots_to_remove:
            all_time_dict.pop(str(slot), None)
    context = {
        'today': today.isoformat(),
        'available_slots': all_time_dict,
        'date': datetime.date.fromisoformat(day),
        'day': day, 'user_id': user_id,
        'times': times,
    }
    if request_time:
        times.append(request_time)
        times.sort()
        return HttpResponseClientRedirect(reverse('time', args=(day, user_id)))
    return render(request, 'time_slots.html', context)


def remove_cart(request, pk):
    cart = Cart(request)
    cart.clear()
    appointment = Appointment.objects.get(pk=pk)
    appointment_items = AppointmentItem.objects.filter(appointment=appointment)
    for item in appointment_items:
        item.delete()
    appointment.services_price = 0
    appointment.save()
    return redirect('confirm_date_time', pk)


def get_rotenburo_times(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    date = appointment.date
    start_time = datetime.time.isoformat(appointment.start_time)[:5]
    end_time = datetime.time.isoformat(appointment.end_time)[:5]
    all_time_dict = {}
    for key in range(int(start_time[:2]), int(end_time[:2])):
        all_time_dict.update(
            {str(key): str(key) + ':' + '00' + '-' + str(key + 1)+'-'+'00'})
    context = {'appointment': appointment, 'available_slots': all_time_dict,
               'date': date}
    return render(request, 'rotenburo_times.html', context)
