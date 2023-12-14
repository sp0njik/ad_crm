from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.db import models

from ad_surface.models import Surface


class Company(AbstractUser):
    name: str = models.CharField(max_length=255, verbose_name='Название организации')
    phone_number: str = models.CharField(max_length=11, verbose_name='Номер телефона')
    legal_address: str = models.CharField(max_length=255, verbose_name='Юридический адрес')
    actual_address: str = models.CharField(max_length=255, verbose_name='Фактический адрес')
    is_agency: bool = models.BooleanField(default=False, verbose_name='Агенство')
    agency: 'Company' = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True,
                                          verbose_name='Агенство')
    placement: list[Surface] = models.ManyToManyField(Surface, through='Placement', verbose_name='Размещение')


class Placement(models.Model):
    surface: Surface = models.ForeignKey(Surface, on_delete=models.PROTECT, related_name='orders',
                                         verbose_name='Поверхность')
    company: Company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='placements',
                                         verbose_name='Организация')
    start_at: datetime = models.DateField(verbose_name='Дата начала размещения')
    duration: timedelta = models.DurationField(verbose_name='Продолжительность размещения')
    invoice: File = models.FileField(upload_to='files', blank=True, verbose_name='счет на оплату')
    reconciliation: File = models.FileField(upload_to='files', null=True, blank=True, verbose_name='Акт сверки')

    def finish_at(self):
        return self.start_at + self.duration

    def __str__(self):
        return self.company.name


class PlacementFile(models.Model):
    file: File = models.FileField(upload_to='files')
    placement: Placement = models.ForeignKey(Placement, on_delete=models.CASCADE)
