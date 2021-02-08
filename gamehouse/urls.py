from django.views.generic import TemplateView as tv
from django.urls import path, include, re_path,reverse

from gamehouse.sjug.views import universales
from gamehouse.sjug.views import juego as sjug_juego
from decouple import config
from django.conf import settings
from django.conf.urls.static import static

urls_universales = [
    path('', tv.as_view(template_name="homepage.html"), name='index'),  
    path('login/',universales.login, name='login'),
    path('registro/', universales.registro, name= 'registro'),
    path('logout/',universales.logout, name='logout'), 
    path('error/403',universales.solicitud_denegada,name='error_403'),
    path('error/404',universales.no_encontrado,name='error_404'),
    
    path('consolas/',tv.as_view(template_name="juegos/consolas.html"), name="consolas"),
    path('generos/',tv.as_view(template_name="juegos/generos.html"), name="generos"),
    path('InfConsolas/',tv.as_view(template_name="juegos/InfoConsolas.html"), name='InfConsolas'),
    path('InfGeneros/', tv.as_view(template_name="juegos/InfoGeneros.html"), name='InfGeneros'),
    path('juegos/',sjug_juego.juegos, name = 'juegos'),
    path('Busqueda/',sjug_juego.busqueda, name = 'busqueda'),
    path('juegos/<int:id_juego>',sjug_juego.ver_juego,name='ver_juego'), #Ver el juego y un snippet de opiniones
    path('juegos/<jugador>/agregar_videojuego/<int:id_juego>/',sjug_juego.agregar_videojuego,name='agregar_videojuego'), #Ver el juego y un snippet de opiniones
    path('juegos/<int:id_juego>/opiniones',sjug_juego.ver_juego,name='opiniones'), #Lista de opiniones
   # path('juegos/<int:id_juego>/opiniones/<jugador>',sjug_juego.opiniones_jugador,name='opiniones_juego'), #Ver la opinion de cierto juego
   # path('juegos/<int:id_juego>/opiniones/<jugador>/crear',sjug_juego.ver_juego,name='ver_juego'),
   # path('juegos/<int:id_juego>/opiniones/<jugador>/eliminar',sjug_juego.ver_juego,name='ver_juego'),
    
]

urlpatterns = [
    path('',include(urls_universales)),
    path('sjug/',include('gamehouse.sjug.urls')),
    path('sadm/',include('gamehouse.sadm.urls')),
    #### Seccion pruebas
    path('algoritmos/',universales.algoritmos,name='algoritmos'),
    path('descripciones/',universales.limpiar_descripciones,name='limpiar_descripciones'),
    path('tf-idf-propio/',universales.tf_idf_propio,name='vec_tf_idf'),
    path('tf-idf-sk/',universales.tf_idf_sk,name='vec_tf_idf_sk'),
    path('obtener-cpus/',universales.obtener_cpus,name='obtener_cpus'),
    path('generar-tf-idf/', universales.generar_tf_idf , name='generar_tf_idf'),
    path('contar_caracteristicas/',universales.contar_caracteristicas,name='contar_caracteristicas'),
    path('crear_vector_perfil/',universales.crear_vector_perfil,name='crear_vector_perfil'),
    path('actualizar-direccion/', universales.actualizar_direccion, name="actualizar_direccion"),
    path('vector_genero_plataforma/', universales.vector_genero_plataforma, name="vector_genero_plataforma"),
    path('recomendacion-genero/', universales.generar_rec_genero, name="generar_rec_genero"),
    path('recomendacion-plataforma/', universales.generar_rec_plataforma, name="generar_rec_plataforma"),
    path('normalizar-vectores/', universales.normalizar_vectores, name="normalizar_vectores"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

""" 
if settings.ADMIN_ENABLED is True:
	from django.contrib import admin
	urlpatterns += [path('admin/', admin.site.urls),]




	ACTIVACION DE ADMIN DJANGO:

Para modo local

if settings.ADMIN_ENABLED is True:
	from django.contrib import admin
	urlpatterns += [path('admin/', admin.site.urls),]
  
Para modo produccion:
 ADMIN_ENABLED = config('ADMIN_ENABLED', default=False, cast=bool)
 if ADMIN_ENABLED is True:
	from django.contrib import admin
	urlpatterns += [path('admin/', admin.site.urls),]

	ACTIVAR ACCESO A ARCHIVOS ESTATICOS

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
