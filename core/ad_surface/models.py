from django.core.files.images import ImageFile
from django.db import models


class Surface(models.Model):
    name: str = models.CharField(max_length=255, verbose_name='Наименование поверхности')
    description: str = models.TextField(verbose_name='Описание поверхности')
    width: int = models.IntegerField(verbose_name='Ширина, м')
    height: int = models.IntegerField(verbose_name='Высота, м')
    price: int = models.IntegerField(verbose_name='Стоимость')
    address: str = models.CharField(max_length=255, verbose_name='Адрес поверхности')
    place: str = models.CharField(max_length=255, verbose_name='Месторасположение')
    is_active: bool = models.BooleanField(default=False, verbose_name='Активно')

    def __str__(self):
        return self.name

    def square(self) -> int:
        return self.width * self.height


class SurfaceImage(models.Model):
    image: ImageFile = models.ImageField(upload_to='surfaces', verbose_name='Изображение')
    surface: Surface = models.ForeignKey(Surface, on_delete=models.CASCADE)
