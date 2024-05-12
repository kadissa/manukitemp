import datetime
from pprint import pprint
from django_htmx.http import HttpResponseClientRedirect
from django.contrib import messages
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from .models import Customer, Appointment
from .forms import ItemForm, AppointmentForm, CustomerForm
from django.utils import timezone

times = set()
date = None


class HTTPResponseHXRedirect(HttpResponseRedirect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["HX-Refresh"] = self["Location"]

    status_code = 200


def get_day(request):
    print('function get_day')

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
    if request.GET.get('date'):
        request_date = request.GET.get('date')
        context = {
            'min_day': min_day_value, 'max_day': max_day_value,
            'available_slots': all_time_dict.values(),
            'today': today.isoformat(),
            'date': datetime.date.fromisoformat(request_date).strftime(
                '%d-%m-%Y')

        }
    else:
        context = {
            'min_day': min_day_value, 'max_day': max_day_value,
            'available_slots': all_time_dict.values(),
            'today': today.isoformat(),
        }

    return render(request, 'temp.html', context)


def appointment_create(request):
    global date
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
    min_day_value = today.isoformat()
    max_day_value = today + datetime.timedelta(days=90)
    if request.GET.get('date'):
        date = request.GET.get('date')
    request_date = request.GET.get('date')
    request_time = request.POST.get('time')
    if request_time:
        times.add(request_time)
    print(f'request_date={request_date}')
    print(f'date={date}')
    print(f'times={times}')
    if date:
        appointments = Appointment.objects.filter(
            date=datetime.date.fromisoformat(date))
        for appointment in appointments:  # get available slots for booking
            start = (appointment.start_time.isoformat('hours'))
            end = appointment.end_time.isoformat('hours')
            if start == '11':
                slots_to_remove = range(int(start), int(end) + 1)
            elif start == '22':
                slots_to_remove = range(int(start) - 1, int(end))
            else:
                slots_to_remove = range(int(start) - 1, int(end) + 1)
            for slot in slots_to_remove:
                all_time_dict.pop(str(slot))
        context = {
            'min_day': min_day_value, 'max_day': max_day_value,
            'available_slots': all_time_dict.values(),
            'today': today.isoformat(),
            'date': datetime.date.fromisoformat(date),
            'times': times

        }
        return render(request, 't_slot.html', context)
    else:
        print(f'if not request_date: date={date}')

        context = {
            'min_day': min_day_value, 'max_day': max_day_value,
            'available_slots': all_time_dict.values(),
            'today': today.isoformat(),
            'date': datetime.date.today()

        }
    if request.method == 'POST':
        pprint(request.POST.get('time'))
        context = {'min_day': min_day_value, 'max_day': max_day_value,
                   'available_slots': all_time_dict.values(),
                   'today': today.isoformat(),
                   'date': datetime.date.fromisoformat(date)
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


def get_user_and_services(request):
    print('function get_user_and_services')
    services_form = ItemForm(request.POST or None)
    if services_form.is_valid():
        services_form.save()
        messages.success(request, 'Successful!')
        return redirect('success')
    context = {
        # 'customer_form': customer_form,
        'services_form': services_form}
    return render(request, 'finish_enter.html', context)


def get_user_and_date(request):
    print('function get_user_and_date')
    request_date = request.POST.get('date')
    form = CustomerForm(request.POST or None)

    if form.is_valid():
        print('form=', form.cleaned_data)
        form.save(commit=False)

        if not Customer.objects.filter(
                phone=form.cleaned_data['phone']).exists():
            form.save()
        return redirect('time', request_date)
    global date
    global times
    times = set()
    date = None
    today = datetime.date.today()
    min_day_value = today.isoformat()
    max_day_value = today + datetime.timedelta(days=60)
    date = request_date
    print(date)
    context = {
        'min_day': min_day_value, 'max_day': max_day_value,
        'today': today.isoformat(), 'form': form,
    }
    if request_date:
        context.update(
            {'date': datetime.date.fromisoformat(request_date).strftime(
                '%d-%m-%Y')})
        return redirect('time', request_date)
    pprint(context)
    return render(request, 'user.html', context)


def get_date(request):
    print('function get_date')

    global date
    global times
    times = set()
    date = None
    today = datetime.date.today()
    min_day_value = today.isoformat()
    max_day_value = today + datetime.timedelta(days=60)
    request_date = request.GET.get('date')
    date = request_date
    print(date)
    if request_date:
        context = {
            'min_day': min_day_value, 'max_day': max_day_value,
            'today': today.isoformat(),
            'date': datetime.date.fromisoformat(request_date).strftime(
                '%d-%m-%Y')

        }
        return redirect('time', request_date)
    else:
        context = {
            'min_day': min_day_value, 'max_day': max_day_value,
            'today': today.isoformat(),

        }
    return render(request, 'includes/date_choice.html', context)


def get_time(request, day):
    print('function get_time')

    global times
    all_time_dict = {'11': '11:00-12:00', '12': '12:00-13:00',
                     '13': '13:00-14:00',
                     '14': '14:00-15:00', '15': '15:00-16:00',
                     '16': '16:00-17:00',
                     '17': '17:00-18:00', '18': '18:00-19:00',
                     '19': '19:00-20:00',
                     '20': '20:00-21:00', '21': '21:00-22:00',
                     '22': '22:00-23:00'}
    print(f'date={day}')
    today = datetime.date.today()

    request_time = request.POST.get('time')
    print(f'request_time={request_time}')
    appointments = Appointment.objects.filter(
        date=datetime.date.fromisoformat(day))
    for appointment in appointments:  # get available slots for booking
        start = (appointment.start_time.isoformat('hours'))
        end = appointment.end_time.isoformat('hours')
        if start == '11':
            slots_to_remove = range(int(start), int(end) + 1)
        elif start == '22':
            slots_to_remove = range(int(start) - 1, int(end))
        else:
            slots_to_remove = range(int(start) - 1, int(end) + 1)
        for slot in slots_to_remove:
            all_time_dict.pop(str(slot))
    context = {
        'today': today.isoformat(),
        'available_slots': all_time_dict,
        'date': datetime.date.fromisoformat(day)
    }
    if request_time:
        times.add(request_time)
        context['times'] = times
        context['truly'] = 'truly'
        messages.success(request, 'successes')
        print(f'context={context}')
        print(f'request_method=post')
        print(times)
        return HttpResponseClientRedirect(reverse('time', args=(day,)))

    context['times'] = times

    print(f'times={times}')
    return render(request, 'includes/time_slots.html', context)
