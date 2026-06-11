from django.db import models

# Create your models here.
class Spell(models.Model):
    name = models.CharField(max_length=256, verbose_name='Заклинание')
    spell_lvl = models.IntegerField(verbose_name='Уровень')
    desc = models.TextField(verbose_name='Описание')
    add_date = models.DateField(verbose_name='Дата добавления')
    def __str__(self):
        return f'{self.name}, Уровень {self.spell_lvl}'
