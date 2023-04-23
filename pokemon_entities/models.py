from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='image', blank=True)
    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.PROTECT)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField(null=True)
    health = models.IntegerField(null=True)
    strenght = models.IntegerField(null=True)
    defence = models.IntegerField(null=True)
    stamina = models.IntegerField(null=True)