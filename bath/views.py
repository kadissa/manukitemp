import datetime
from pprint import pprint

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView

from .models import Customer, Appointment
from .forms import ItemForm, AppointmentForm, CustomerForm
from django.utils import timezone


def temp(request):
    app = Appointment.objects.all()
    context = {'context': 'context', 'app': app}
    return render(request, 'temp.html', context)


def appointment_create(request):
    all_time_dict = {'11': '11:00-12:00', '12': '12:00-13:00',
                     '13': '13:00-14:00',
                     '14': '14:00-15:00', '15': '15:00-16:00',
                     '16': '16:00-17:00',
                     '17': '17:00-18:00', '18': '18:00-19:00',
                     '19': '19:00-20:00',
                     '20': '20:00-21:00', '21': '21:00-22:00',
                     '22': '22:00-23:00'}

    today = datetime.date.today()
    min_day_value = today.isoformat()
    max_day_value = today + datetime.timedelta(days=90)
    request_date = request.GET.get('date')
    request_time = request.GET.get('time')
    print(request_time)
    if request_date:
        appointments = Appointment.objects.filter(
            date=datetime.date.fromisoformat(request_date))
        for appointment in appointments:  # get available slots for booking
            start = appointment.start_time.isoformat('hours')
            end = appointment.end_time.isoformat('hours')
            slots_to_remove = range(int(start), int(end) + 1)
            for slot in slots_to_remove:
                all_time_dict.pop(str(slot))
        context = {
            'min_day': min_day_value, 'max_day': max_day_value,
            'available_slots': all_time_dict.values(),
            'today': today.isoformat(),
            'date': datetime.date.fromisoformat(request_date).strftime(
                '%d-%m-%Y')

        }
        return render(request, 'includes/time_slots.html', context)
    else:
        context = {
            'min_day': min_day_value, 'max_day': max_day_value,
            'available_slots': all_time_dict.values(),
            'today': today.isoformat(),

        }
    print(request_date)
    if request.method == 'POST':
        pprint(request.POST.get('time'))
        context = {'min_day': min_day_value, 'max_day': max_day_value,
                   'available_slots': all_time_dict.values(),
                   'today': today.isoformat(),
                   }
    # if request.method == 'POST':
    #     time = request.POST.get('time')
    #     start_time = time.split('-')[0]
    #     end_time = time.split('-')[1]
    #     # request_date = request.POST.get('date')
    #     customer, created = Customer.objects.update_or_create(
    #         defaults={'email': request.POST.get('email'),
    #                   'phone': request.POST.get('phone')},
    #         name=request.POST.get('name')
    #     )
    #     appointment, created = Appointment.objects.update_or_create(
    #         defaults={
    #             'start_time': start_time,
    #             'date': request.POST.get('date'),
    #             'end_time': end_time,
    #             'price': 21,
    #         },
    #         date=datetime.date.fromisoformat(request_date), customer=customer)

    return render(request, 'appointment_create.html', context)


def items_view(request, pk):
    instance = get_object_or_404(Appointment, pk=pk)
    form = ItemForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successful!')
        return redirect('success')
    context = {'form': form}
    return render(request, 'guest_self_edit.html', context)


def success(request):
    return render(request, 'success.html')


def get_finish(request):
    form = CustomerForm(request.POST or None)
    print(request.POST.get('name'))
    if form.is_valid():
        form.save()
        messages.success(request, 'Successful!')
        return redirect('success')
    context = {'form': form, 'as': '11:00-12:00'}
    return render(request, 'finish_enter.html', context)