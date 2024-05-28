import datetime
import time
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
    for product in products:
        quantity = request.POST.get(f'{product}')
        cart.add_product(product=product, quantity=quantity)
    if request.method == 'POST':
        for item in cart.cart:
            AppointmentItem.objects.create(
                appointment=Appointment.objects.get(pk=pk),
                product=Product.objects.get(name=item),
                price=cart.cart[item]['price'],
                quantity=cart.cart[item]['quantity'],
            )
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
    cart_price = cart.get_total_price()
    appointment.items_price = cart_price
    appointment.save()
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
    times_formated = sorted(times)
    price = get_price(day, times)
    start_time = datetime.time.fromisoformat(times_formated[0][:5])
    end_time = datetime.time.fromisoformat(times_formated[-1][6:])
    customer = Customer.objects.get(pk=user_id)
    appointment = Appointment.objects.update_or_create(
        date=day, customer=customer, start_time=start_time,
        end_time=end_time, status='Не подтверждён', price=price
    )
    times = list()
    if appointment:
        return redirect('confirm_date_time', appointment[0].id)
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
        sorted_times = sorted(times)
        return HttpResponseClientRedirect(reverse('time', args=(day, user_id)))

    return render(request, 'time_slots.html', context)
