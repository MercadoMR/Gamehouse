from django.db.models import *
from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.core.validators import MaxValueValidator, MinValueValidator
#from django.template.defaultfilters import slugify
from django.utils.text import slugify
#from multiselectfield import MultiSelectField
import datetime
import os
from django.utils import timezone


class Plataforma(models.Model):
    id_plataforma = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']


class Genero(models.Model):
    id_genero = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Compania(models.Model):
    id_compania = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Juego(models.Model):
    id_juego = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    anio = models.PositiveIntegerField(default=2020) #Tipo Date >:( 
    descripcion = models.TextField()
    descripcion_limpia = models.TextField(blank = True, null = True)    
    generos = models.ManyToManyField(Genero,
                                     through='GenerosAsociados',
                                     through_fields=('juego', 'genero')
                                     )
    plataformas = models.ManyToManyField(Plataforma,
                                         through='PlataformasAsociadas',
                                         through_fields=('juego', 'plataforma')
                                         )
    companias = models.ManyToManyField(Compania,
                                       through='CompaniasAsociadas',
                                       through_fields=('juego', 'compania')
                                       )

    def __str__(self):
        # return '%s, %s, %s' % (self.titulo, self.jgeneros, self.jplataformas)
        return self.titulo

    def slug(self):
        return slugify(self.titulo, allow_unicode=True)
    
    def save(self, *args, **kwargs):
        if not self.descripcion_limpia: #Si no tienen descripcion limpia
            from gamehouse.algorithms.tf_idf import clean_description
            self.descripcion_limpia = clean_description(self.descripcion)
        super(Juego, self).save(*args, **kwargs)

class Imagen(models.Model):
    id_imagen = models.AutoField(primary_key=True)
    referencia = models.URLField(max_length=511)
    alt = models.CharField(
        max_length=200,
        verbose_name="Texto alternativo a la imagen")
    juego = models.ForeignKey(Juego,
                              on_delete=models.CASCADE,
                              db_column='juego',
                              related_name='imagenes',
                              verbose_name='Imagenes que representan el juego',
                              )


""" Entidades de relacion """


class GenerosAsociados(models.Model):
    # id_gAsociados = models.AutoField(primary_key = True)
    genero = models.ForeignKey(Genero,
                               on_delete=models.CASCADE,
                               db_column='genero',
                               related_name='juegos_asociados',
                               verbose_name='Generos que conforman el juego',
                               )
    juego = models.ForeignKey(Juego,
                              on_delete=models.CASCADE,
                              null=True,
                              db_column='juego',
                              related_name='generos_asociados',
                              verbose_name='Juegos que pertenecen al genero',
                              )

    def __str__(self):
        return self.genero


class ListGeneros(models.Model):
    juego = models.ForeignKey(Juego,
                              on_delete=models.CASCADE,
                              db_column='juego',
                              null=True,
                              related_name='generos_boolean',
                              verbose_name='generos en boolean',
                              )
    listgenero = models.CharField(max_length=200)
    listplataforma = models.CharField(max_length=200)

    def __str__(self):
        return self.juego


class PlataformasAsociadas(models.Model):
    # id_pAsociadas = models.AutoField(primary_key = True)
    plataforma = models.ForeignKey(Plataforma,
                                   on_delete=models.CASCADE,
                                   db_column='plataforma',
                                   related_name='juegos_asociados',
                                   verbose_name='Plataforma a las que pertenece el juego',
                                   )
    juego = models.ForeignKey(Juego,
                              on_delete=models.CASCADE,
                              null=True,
                              db_column='juego',
                              related_name='plataformas_asociadas',
                              verbose_name='Juegos que pertenecen a la plataforma',
                              )

    def __str__(self):
        return self.plataforma


class CompaniasAsociadas(models.Model):
    # id_pAsociadas = models.AutoField(primary_key = True)
    compania = models.ForeignKey(Compania,
                                 on_delete=models.CASCADE,
                                 db_column='compania',
                                 related_name='juegos_asociados',
                                 verbose_name='Compañias que hicieron el juego',
                                 )
    juego = models.ForeignKey(Juego,
                              on_delete=models.CASCADE,
                              null=True,
                              db_column='juego',
                              related_name='companias_asociadas',
                              verbose_name='Juegos que pertenecen a la plataforma',
                              )

    def __str__(self):
        return self.compania


""" Tablas sin usarse """


class Generacion(models.Model):
    id_generacion = models.AutoField(primary_key=True)
    # Introducir las generaciones como primera, septima y asi
    generacion = models.CharField(unique=True,
                                  null=False,
                                  max_length=20,
                                  verbose_name="Numero de generacion")
    # Numero de bits de esta generacion
    # https://www.tecnobreak.com/generaciones-videoconsolas/
    # https://gamedev.stackexchange.com/questions/114381/8-16-32-bits-consoles-what-does-it-mean
    bits = models.PositiveIntegerField(default=4, blank=True,
                                       validators=[
                                           MinValueValidator(1), MaxValueValidator(2056)]
                                       )
    # Periodos
    inicio = models.DateField()
    fin = models.DateField()


""" Viejos comentarios """
"""
      campo_slug = models.SlugField (
        verbose_name = "Representacion slug del titulo",
        allow_unicode = True,
        unique=True,
        blank = True,
        null = True)
    """
"""
      def save(self, *args, **kwargs):
        if not self.campo_slug: self.campo_slug = slugify(self.titulo)
        super(Juego, self).save(*args, **kwargs)
    """
# def Obt_Gen(self):
#   OGeneros=str([ogenero for generos in self.generos.all().values_list('nombreG',flat=True)]).replace("[","").replace("]","").replace("'","")
#   return OGeneros

# def Obt_Plat(self):
#   OPlataforma=str([oplataforma for plataformas in self.plataformas.all().values_list('nombreP',flat=True)]).replace("[","").replace("]","").replace("'","")
#   return OPlataforma
