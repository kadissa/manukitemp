import datetime
from pprint import pprint

from django.views.decorators.http import require_POST
from django_htmx.http import HttpResponseClientRedirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from .cart import Cart
from .models import Customer, Appointment, Item, Product
from .forms import ItemForm, AppointmentForm, CustomerForm, CartAddProductForm
from django.utils import timezone

times = list()


def error(request):
    return render(request, 'error.html')


def product_list(request):
    cart = Cart(request)
    products = Product.objects.all()
    print('if request.method == POST1')

    for product in products:
        print('if request.method == POST2')
        quantity = request.POST.get(f'{product}')
        cart.add(product=product, quantity=quantity)
        pprint(cart.__dict__)
    total_price = cart.get_total_price()
    print(f'total price: {total_price}')
    if request.method == 'POST':
        return redirect('cart')
    print(request.session['cart'])

    context = {
        'products': products,
        'cart': cart
    }

    return render(request, 'products.html', context)


def cart_detail(request):
    cart_instance = Cart(request)
    cart = request.session['cart']
    # total_price = cart.get_total_price()
    return render(request, 'cart_detail.html', {'cart': cart,
                                                # 'total_price': total_price
                                                'cart_instance': cart_instance})


# def items_view(request, pk):
#     appointment = get_object_or_404(Appointment, pk=pk)
#     form = ItemForm(request.POST or None)
#     form.set_label_rotenburo(x=2000)
#     print(f'appointmen.customer: {appointment.customer}')
#     if form.is_valid():
#         if not appointment.items:
#             item = form.save(commit=False)
#             item.name = appointment.customer
#
#             form.save()
#             # item.save()
#             appointment.items = item
#             appointment.save()
#             return redirect('confirm_items', pk=pk)
#         else:
#             messages.error(request, 'Вы не можете редактировать список доп. '
#                                     'услуг, пожалуйста обратитесь к '
#                                     'администратору')
#     context = {'form': form, 'appoint_id': pk}
#     return render(request, 'service.html', context)


def finish_view(request, appoint_id):
    appointment = get_object_or_404(Appointment, pk=appoint_id)
    context = {'appointment': appointment}
    return render(request, 'confirm_date_time.html', context)


def create_appointment(request, day, user_id):
    global times
    if not day or not times:
        return redirect('error')
    times_formated = sorted(times)
    start_time = datetime.time.fromisoformat(times_formated[0][:5])
    end_time = datetime.time.fromisoformat(times_formated[-1][6:])
    customer = Customer.objects.get(pk=user_id)
    appointment = Appointment.objects.update_or_create(
        date=day, customer=customer, start_time=start_time,
        end_time=end_time, status='Не подтверждён', price=2000 * len(times),
    )
    times = list()
    if appointment:
        return redirect('finish', appointment[0].id)
    else:
        return redirect('error')


def get_customer_and_date(request):
    request_date = request.POST.get('date')
    print(f'request.session: {request.session.items()}')
    customer_id = request.session.get('customer_id', 0)
    if Customer.objects.filter(id=customer_id).exists():
        customer = get_object_or_404(Customer,
                                     id=request.session['customer_id'])
        form = CustomerForm(request.POST or None, instance=customer)
    else:
        form = CustomerForm(request.POST or None)
    global times
    times = list()
    if form.is_valid():
        if not Customer.objects.filter(
                phone=form.cleaned_data['phone'], ).exists():
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
        'day': day, 'user_id': user_id
    }
    if request_time:
        times.append(request_time)
        sorted_times = sorted(times)
        context['times'] = times
        return HttpResponseClientRedirect(reverse('time', args=(day, user_id)))

    context['times'] = times
    return render(request, 'includes/time_slots.html', context)


def confirm_items(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    item_id = appointment.items_id
    items = Item.objects.filter(id=item_id)
    context = {'appointment': appointment, 'items': items}
    return render(request, 'confirm_items.html', context)
