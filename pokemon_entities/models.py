from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя')
    image = models.ImageField(upload_to='image', blank=True, verbose_name='Изображение')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Имя на английском')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='Имя на японском')
    description = models.TextField(blank=True, verbose_name='Описание')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="kids", verbose_name='Эволюция')
    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.PROTECT, verbose_name='Покемон')
    lat = models.FloatField(null=True,blank=True, verbose_name='Широта')
    lon = models.FloatField(null=True,blank=True, verbose_name='Долгота')
    appeared_at = models.DateTimeField(null=True,blank=True, verbose_name='Дата и время появления')
    disappeared_at = models.DateTimeField(null=True,blank=True, verbose_name='Дата и время исчезновения')
    level = models.IntegerField(null=True,blank=True, verbose_name='Уровень')
    health = models.IntegerField(null=True,blank=True, verbose_name='Здоровье')
    strenght = models.IntegerField(null=True,blank=True, verbose_name='Атака')
    defence = models.IntegerField(null=True,blank=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, blank=True,verbose_name='Выносливость')
    def __str__(self):
        return self.pokemon.title