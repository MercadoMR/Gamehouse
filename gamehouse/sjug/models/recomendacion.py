from django.db.models import *
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .juego import Juego
from .jugador import Jugador

# La recomendacion es un conjunto de listas de juegos de diferentes tematicas


class Recomendacion(models.Model):
    id_recomendacion = models.AutoField(primary_key=True)
    tipo = models.CharField(
        max_length=30,
        verbose_name="Tipo de recomendación")
    jugador = models.ForeignKey(Jugador,
                                on_delete=models.CASCADE,
                                to_field='nickname',
                                related_name='recomendaciones',
                                db_column='jugador',
                                verbose_name='Jugador al que se le hace esta recomendacion',
                                )
    # Calificacion del usuario del 1 al 10 indicando que tanto le gusto este
    # conjunto de listas
    retroalimentacion = models.PositiveIntegerField(default=1, null = True , 
                                                    blank=True,
                                                    validators=[
                                                        MinValueValidator(1), MaxValueValidator(10)]
                                                    )


class Lista(models.Model):
    id_lista = models.AutoField(primary_key=True)
    titulo = models.CharField(
        max_length=50,
        verbose_name="El nombre de la lista")
    
    juegos = models.ManyToManyField(
        Juego, verbose_name="Juegos que conforman esta lista")
    
    recomendacion = models.ForeignKey(Recomendacion,
                                      on_delete=models.CASCADE,
                                      related_name='listas',
                                      db_column="id_recomendacion",
                                      verbose_name='Recomendacion a la que pertenece esta lista',
                                      )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripcion detallada de la lista si existe")
    "Juegos que se parecen a DOOM 64"

# Ejemplo de modelado Muchos a muchos
"""
class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
"""
