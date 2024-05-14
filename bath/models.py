from django.core.validators import MinValueValidator, EmailValidator
from django.db import models


class Customer(models.Model):
    name = models.CharField('Имя', max_length=60)
    surname = models.CharField('Фамилия', max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=60,
                              validators=[EmailValidator()],
                              blank=True,
                              null=True)
    phone = models.CharField('Телефон', max_length=15)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.ForeignKey(Customer, on_delete=models.CASCADE,
                             verbose_name='Гость', related_name='items',
                             error_messages='Не заполнено поле name')
    rotenburo = models.PositiveSmallIntegerField('Ротэнбуро', blank=True,
                                                 null=True,
                                                 # help_text='Количество часов'
                                                 )
    birch_broom = models.PositiveSmallIntegerField('Веник берёза',
                                                   blank=True,
                                                   null=True,
                                                   # help_text='штук'
                                                   )
    oak_broom = models.PositiveSmallIntegerField('Веник дуб', blank=True,
                                                 null=True,
                                                 # help_text='штук'
                                                 )
    bed_sheet = models.PositiveSmallIntegerField('Простыня', blank=True,
                                                 null=True,
                                                 # help_text='штук'
                                                 )
    towel = models.PositiveSmallIntegerField('Полотенце', blank=True,
                                             null=True,
                                             # help_text='штук'
                                             )
    robe = models.PositiveSmallIntegerField('Халат', blank=True, null=True,
                                            # help_text='штук'
                                            )
    slippers = models.PositiveSmallIntegerField('Тапки', blank=True, null=True,
                                                # help_text='штук'
                                                )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def price(self):
        self.oak_broom_price = self.oak_broom * 300
        return self.oak_broom_price

    class Meta:
        verbose_name = 'Доп. услуга'
        verbose_name_plural = 'Доп. услуги'


class Appointment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 verbose_name='Гость')
    items = models.ForeignKey(Item, on_delete=models.CASCADE,
                              verbose_name='Аксессуары', blank=True,
                              null=True, related_name='appointments')
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f'Бронь {self.id}. Гость-{self.customer.name}'

    # def get_absolute_url(self):
    #     return reverse('bnovo:sauna_detail', kwargs={'pk': self.id})
