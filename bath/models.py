from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
# from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    name = models.CharField('Имя', max_length=60)
    surname = models.CharField('Фамилия', max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=60, blank=True, null=True)
    phone = models.PositiveSmallIntegerField('Телефон')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name


class Appointment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 verbose_name='Гость')
    status = models.CharField('Статус', max_length=60, blank=True, null=True)
    date = models.DateField()
    start_time = models.TimeField('Начало')
    end_time = models.TimeField('Конец')
    duration = models.CharField('Продолжительность', max_length=60, blank=True)
    price = models.PositiveSmallIntegerField('Стоимость бани')
    appointment_full_price = models.PositiveSmallIntegerField('Стоимость '
                                                              'заказа рублей',
                                                              blank=True,
                                                              null=True)
    amount = models.PositiveSmallIntegerField('Количество',
                                              blank=True,
                                              null=True, default=2,
                                              validators=[MinValueValidator(
                                                  2)])
    source = models.CharField('Источник', max_length=60, blank=True, null=True)
    full_name = models.CharField('Полное имя', max_length=60, blank=True,
                                 null=True)
    comment = models.CharField('Комментарий', max_length=60, blank=True,
                               null=True)
    tag = models.CharField('Примечание', max_length=200, blank=True, null=True)
    people_count = models.PositiveSmallIntegerField('Кол-во чел.',
                                                    blank=True, null=True)
    prepayment = models.PositiveSmallIntegerField('Предоплата', blank=True,
                                                  null=True)
    # services = models.ManyToManyField(Service, related_name='appointments',
    #                                   # through='Order',
    #                                   verbose_name='Услуги')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f'Бронь {self.id}. Гость-{self.customer.name}'

    # def get_absolute_url(self):
    #     return reverse('bnovo:sauna_detail', kwargs={'pk': self.id})


# class Service(models.Model):
#     appointments = models.ForeignKey(Appointment, on_delete=models.CASCADE,
#                                      related_name='services',
#                                      verbose_name='Номер заказа', null=True,
#                                      blank=True)
#     name = models.CharField('Название', max_length=50)
#     duration = models.DurationField(blank=True, null=True)
#     measurement_unit = models.CharField('Ед изм', max_length=200,
#                                         null=True)
#     amount = models.PositiveSmallIntegerField('Кол', blank=True,
#                                               null=True)
#     price = models.PositiveSmallIntegerField('Цена', default=100)
#     full_price = models.PositiveSmallIntegerField(null=True, blank=True)
#     description = models.CharField('Описание', max_length=200, blank=True,
#                                    null=True)
#     available = models.BooleanField(default=True)
#     slug = models.SlugField(blank=True)
#
#     class Meta:
#         verbose_name = 'Доп Услуга'
#         verbose_name_plural = 'Доп Услуги'
#
#     def __str__(self):
#         return self.name
#
#     def save(self, *args, **kwargs):
#         self.full_price = self.price * (self.amount or 0)
#         super(Service, self).save(*args, **kwargs)
#     class Meta:
#         verbose_name = 'Аксессуары'

class Item(models.Model):
    appointments = models.ForeignKey(Appointment, on_delete=models.CASCADE,
                                     related_name='items',
                                     verbose_name='Номер заказа')
    rotenburo = models.PositiveSmallIntegerField('Ротэнбуро', blank=True,
                                                 null=True,
                                                 help_text='Количество часов')
    birch_broom = models.PositiveSmallIntegerField('Веник бер.', blank=True,
                                                   null=True, help_text='штук')
    oak_broom = models.PositiveSmallIntegerField('Веник дуб', blank=True,
                                                 null=True, help_text='штук')
    bed_sheet = models.PositiveSmallIntegerField('Простыня', blank=True,
                                                 null=True, help_text='штук')
    towel = models.PositiveSmallIntegerField('Полотенце', blank=True,
                                             null=True, help_text='штук')
    robe = models.PositiveSmallIntegerField('Халат', blank=True, null=True,
                                            help_text='штук')
    slippers = models.PositiveSmallIntegerField('Тапки', blank=True, null=True,
                                                help_text='штук')
    created_at = models.DateTimeField(auto_now_add=True, blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, )

    def __str__(self):
        return 'Допы'

    class Meta:
        verbose_name = 'Доп. услуга'
        verbose_name_plural = 'Доп. услуги'
