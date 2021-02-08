from django.contrib import admin
from django.views.generic import TemplateView as tv
from django.urls import path, re_path,include
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from gamehouse.sjug.views import jugador as sjug_jugador
from gamehouse.sjug.views import juego as sjug_juego

"""
CAMBIOS:
ACTUAL | CAMBIO | DESCRIPCION

mis_gustos/<int:id_gustos>/ | /sjug/<jugador>/gustos | Mostrar tres botones: Modificar mis generos, Modificar mis plataformas y Modificar mis juegos
mis_gustos/mis_gustos_2/<int:id>/ | indicado | Mostrar lista mis de juegos, un buscador de juegos y sus opciones añadir, ver y quitar
VVJuego/<int:id_juego>/<int:pk> 
juegos/<int:id_juego>


PENDIENTES:

/sjug/<jugador>/opinion/<int:id_opinion>  Muestra la opinion con id_opinion del jugador indicado
/sjug/<jugador>/opinion/<slug: juego_buscado> Buscar opiniones de la lista de opiniones del jugador indicado cuyo videojuego sea el del slug
                                              Por ejemplo /sjug/Mimir/opinion/grand-theft-auto busca opiniones que tengan que ver con GTA
/sjug/<jugador>/opinion/<int:id_opinion>/eliminar    

 path('',sjug_jugador.inicio ,name="inicio_jugador"), ## /sjug/  
    path('<jugador>/',sjug_jugador.perfil,name='perfil1'), ## /sjug/<jugador> Ver y modificar perfil del jugador
    
    path('<slug:juego_slug>/',sjug_views.juegotal,name="juego"),
"""
    #path('iusuario/',login_required(views.iusuario), name='iusuario'),  ### /sjug/<jugador>/dashboard VEr recom.
#/sjug/
urlpatterns = [
   path('',sjug_juego.default, name = 'sjug'), #Terminada
   path('<jugador>/',sjug_jugador.perfil, name = 'jugador'),
   path('<jugador>/palabras',sjug_jugador.registro_palabras, name = 'registro_palabras'),
   path('<jugador>/editar/',login_required(sjug_jugador.editar_perfil), name = 'editar_jugador'),
   path('<jugador>/eliminar/',login_required(sjug_jugador.eliminar_perfil), name = 'eliminar_jugador'),
   
   path('<jugador>/gusto',login_required(sjug_jugador.gusto), name = 'gusto'),
   path('<jugador>/gusto/gustos',login_required(sjug_jugador.mis_gustos), name = 'mis_gustos'),
   path('<jugador>/gusto/juegos/',login_required(sjug_jugador.mis_juegos), name = 'mis_juegos'),
   path('<jugador>/gusto/juegos/<int:id_juego>/agregar/',login_required(sjug_jugador.agregar_mi_juego), name='agregar_mi_juego'),
   path('<jugador>/gusto/juegos/<int:id_juego>/eliminar/',login_required(sjug_jugador.eliminar_mi_juego), name = 'eliminar_mi_juego'),
   path('<jugador>/gusto/palabras/',login_required(sjug_jugador.mis_palabras), name = 'mis_palabras'),
      
   path('<jugador>/dashboard/',login_required(sjug_jugador.dashboard), name = 'dashboard'), ### /sjug/<jugador>/dashboard  Presentación de recomendaciones
   path('<jugador>/recomendacion_puntuacion/',login_required(sjug_jugador.recomendacion_puntuacion), name = 'recomendacion_puntuacion'), ### /sjug/<jugador>/dashboard  Presentación de recomendaciones   
   path('<jugador>/recomendacion_puntuacion/gusto',login_required(sjug_jugador.recomendacion_puntuacion_gusto), name = 'recomendacion_puntuacion_gusto'), ### /sjug/<jugador>/dashboard  Presentación de recomendaciones   
   path('<jugador>/recomendacion_puntuacion/guion',login_required(sjug_jugador.recomendacion_puntuacion_guion), name = 'recomendacion_puntuacion_guion'), ### /sjug/<jugador>/dashboard  Presentación de recomendaciones   
   path('<jugador>/recomendacion_puntuacion/arte',login_required(sjug_jugador.recomendacion_puntuacion_arte), name = 'recomendacion_puntuacion_arte'), ### /sjug/<jugador>/dashboard  Presentación de recomendaciones   
   path('<jugador>/recomendacion_puntuacion/jugabilidad',login_required(sjug_jugador.recomendacion_puntuacion_jugabilidad), name = 'recomendacion_puntuacion_jugabilidad'), ### /sjug/<jugador>/dashboard  Presentación de recomendaciones   
   path('<jugador>/recomendacion_puntuacion/tecnico',login_required(sjug_jugador.recomendacion_puntuacion_tecnico), name = 'recomendacion_puntuacion_tecnico'), ### /sjug/<jugador>/dashboard  Presentación de recomendaciones   
   path('<jugador>/opiniones/',sjug_jugador.mis_opiniones, name = 'mis_opiniones'),  #Ver mis opiniones de todos los juegos
   path('<jugador>/opinion/',sjug_jugador.opinion, name = 'opinion'),  #Ver mis opiniones de todos los juegos
   #path('<jugador>/opiniones/<genero>/',sjug_juego.opiniones, name = 'mis_opiniones'), ## ver opiniones de cierto genero
   #path('<jugador>/opiniones/<plataforma>/',sjug_juego.opiniones, name = 'mis_opiniones'), ## ver opiniones de cierta plataforma 
    
   path('<jugador>/dashboard/recomendacion/',login_required(sjug_jugador.recomendacion), name = 'recomendacion'),
   path('<jugador>/dashboard/recomendacion/descripcion/',login_required(sjug_jugador.recomendacion_descripcion), name = 'recomendacion_descripcion'),
   path('<jugador>/dashboard/recomendacion/genero/',login_required(sjug_jugador.recomendacion_genero), name = 'recomendacion_genero'),
   path('<jugador>/dashboard/recomendacion/plataforma/',login_required(sjug_jugador.recomendacion_plataforma), name = 'recomendacion_plataforma'),

]

