from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=256, verbose_name='Тэг')

    def __str__(self):
        return f'{self.name}'


class Spell(models.Model):
    name      = models.CharField(max_length=256, verbose_name='Заклинание')
    spell_lvl = models.IntegerField(verbose_name='Уровень')
    desc      = models.TextField(verbose_name='Описание')
    add_date  = models.DateField(verbose_name='Дата добавления')
    image     = models.ImageField(upload_to='spells/', blank=True, null=True, verbose_name='Изображение')
    author    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автор')
    tags      = models.ManyToManyField(Tag, blank=True, related_name='spells', verbose_name='Тэг')

    def __str__(self):
        return f'{self.name}, Уровень {self.spell_lvl}'

    def get_absolute_url(self):
        return reverse('spell_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    spell      = models.ForeignKey(Spell, on_delete=models.CASCADE, related_name='comments', verbose_name='Заклинание')
    author     = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text       = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author} - {self.spell}'
