from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_timestamp_path

class AdvUser(AbstractUser):
   is_activated = models.BooleanField(default=True, db_index=True,
                                      verbose_name='Прошел активацию?')
   send_messages = models.BooleanField(default=True,
                                       verbose_name='Оповещать при новых комментариях?')

   sur_name = models.CharField(max_length=200, blank=False, verbose_name='Фамилия')
   n_name = models.CharField(max_length=200, blank=False, verbose_name='Имя')
   pat_mic = models.CharField(max_length=200, blank=False, verbose_name='Отчество')

   class Meta(AbstractUser.Meta):
       pass


   def delete(self, *args, **kwargs):
       for bb in self.bb_set.all():
           bb.delete()
       super().delete(*args, **kwargs)

   def is_author(self, bb):
       if self.pk == bb.author.pk:
           return True
       return False

   # def clean(self):
   #     if not self.send_messages:
   #         raise ValidationError('Подтвердите согласие на обработку персональных данных')

   class Meta(AbstractUser.Meta):
       pass

class Category(models.Model):
    category_title = models.CharField(max_length=200, verbose_name='Название категории')

    def __str__(self):
        return self.category_title

    # def delete(self, *args, **kwargs):
    #     for request in Applic.objects.filter(category=self):
    #         request.delete()
    #     super(Category, self).delete(*args, **kwargs)

class Applic(models.Model):
    title = models.CharField(max_length=40, verbose_name='Название заявки')
    content = models.TextField(verbose_name='Описание заявки')
    image = models.ImageField(blank=True, upload_to='design1', verbose_name='Изображение')
    data = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    choices = (
        ('Новая', 'Новая'),
        ('Принято в работу', 'Принято в работу'),
        ('Выполнено', 'Выполнено'),
    )
    status = models.CharField(verbose_name="Статус", max_length=70, choices=choices, default='Новая')
    user = models.ForeignKey('AdvUser', on_delete=models.CASCADE, null=False)
    comment = models.TextField(blank=True)
    image_design = models.ImageField(blank=True, upload_to='design/', verbose_name='Фотография')

    def is_completed(self):
        return self.status == 'Выполнено'

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)


    class Meta:
        ordering = ['-data']


class AdditionalImage(models.Model):
    bb = models.ForeignKey(Applic, on_delete=models.CASCADE, verbose_name='Заявка')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Фотография')

class Meta:
    verbose_name_plural = 'Дополнительные иллюстрации'
    verbose_name = 'Дополнительная иллюстрация'

