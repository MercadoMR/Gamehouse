import os
from django.conf import settings
from django.db.models import *
from django.db import models#, FloatField 
from gamehouse.sjug.models import Juego,Usuario,JuegosFavoritos,Opinion


class Administrador(models.Model):
  usuario = models.OneToOneField(Usuario,
                                 on_delete=models.CASCADE,
                                 primary_key=True,
                                 to_field="id_usuario",
                                 db_column="id_administrador",
                                 verbose_name = "Identificador del administrador"
                                 )
  nombre = models.CharField(unique = True,max_length=256)
  #movimiento = DecimalField(null = True)

class MatrizJuegos(models.Model):
  juego = models.OneToOneField(Juego, 
    on_delete = models.CASCADE, 
    primary_key = True,
    db_column = "id_juego",
    verbose_name = "Identificador del juego"
  )
  vector_genero =models.CharField(max_length=256)
  vector_plataforma =models.CharField(max_length=256)
  vector_cpu =models.CharField(max_length=256)
  vector_cde =models.CharField(max_length=256)

  
class Tf_Idf(models.Model):
    juego = models.OneToOneField(Juego, 
                                 on_delete = models.CASCADE, 
                                 primary_key = True,
                                 db_column = "juego",
                                 verbose_name = "Juego del vector tf-idf"
    )
    vector = models.FilePathField(path=settings.ANALITYCS_DIR)
  
""" Funciones """
#https://www.youtube.com/watch?v=Zx09vcYq1oc
#https://www.caktusgroup.com/blog/2017/08/28/advanced-django-file-handling/
    
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)
