from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView as tv
from django.urls import path, re_path,include
from django.shortcuts import redirect
from gamehouse.sadm.views import juegos,jugadores,administrador

urlpatterns = [
    path('<administrador>/',login_required(administrador.perfil_adm), name='perfil_adm'),
    path('<administrador>/videojuegos',login_required(juegos.lista_videojuegos), name='lista_videojuegos'),####################################/sadm/<administrador>/videojuegos   mostrar lista de videojuegos
    path('<administrador>/videojuegos/<int:id_juego>/', login_required(juegos.editar_videojuegos), name='editar_videojuegos'),##################################/sadm/<administrador>/videojuegos/<Int: id_juego >    editar juego con id id_juego
    path('<administrador>/videojuegos/<int:id_juego>/eliminar', login_required(juegos.eliminar_videojuegos), name='eliminar_videojuegos'),############################/sadm/<administrador>/videojuegos/<Int: id_juego >/eliminar   Borrar juego con id_juego         modificar con un alert
    path('<administrador>/videojuegos/nuevo', login_required(juegos.registro_videojuegos), name='registro_videojuegos'),#####################/sadm/<administrador>/videojuegos/nuevo         Agregar un juego nuevo
    path('<administrador>/genero_plataforma', login_required(juegos.genero_plataforma), name='genero_plataforma'),###############################################################/sadm/<administrador>/genero_plataforma   mostrar lista de generos y plataformas
    path('<administrador>/genero_plataforma/registro',login_required(juegos.registro_gen_pla), name='registro_gen_pla'),####################################################/sadm/<administrador>/genero_plataforma/registro      registro de generos y plataformas
    path('<administrador>/plataforma/<int:id_plataforma>/eliminar', login_required(juegos.eliminar_Plataforma), name='eliminar_Plataforma'),###############################/sadm/<administrador>/plataforma/<Int: id_plataforma >/eliminar   Eliminar plataforma    
    path('<administrador>/plataforma/<int:id_plataforma>/', login_required(juegos.editar_Plataforma), name='editar_Plataforma'),###############################################/sadm/<administrador>/plataforma/<Int: id_plataforma >          Editar plataforma
    path('<administrador>/genero/<int:id_genero>/eliminar', login_required(juegos.eliminar_Genero), name='eliminar_Genero'),###############################/sadm/<administrador>/genero/<Int: id_genero >/eliminar         Eliminar genero
    path('<administrador>/genero/<int:id_genero>/', login_required(juegos.editar_Genero), name='editar_Genero'),###############################################/sadm/<administrador>/genero/<Int: id_genero >                  Editar genero
    path('<administrador>/VCPU', login_required(juegos.ViewcaracteristicasPU), name='ViewcaracteristicasPU'),################################### Ver las lista de vectores de los Usuario 
    path('<administrador>/VCDE', login_required(juegos.ViewcaracteristicasDE), name='ViewcaracteristicasDE'),###################################Ver la lista de vectores de caracteristica
    path('<administrador>/jugadores', login_required(jugadores.gestion_usuarios), name='gestion_usuarios'),
    path('<administrador>/jugadores/registro',login_required(jugadores.registro_usuarios), name='registro_usuarios'),
    path('<administrador>/jugadores/<int:id_usuario>/eliminar',login_required(jugadores.eliminar_usuarios), name='eliminar_usuarios'),
    path('<administrador>/jugadores/<int:id_usuario>/',login_required(jugadores.editar_usuarios), name='editar_usuarios'),
    path('<administrador>/signout/',login_required(administrador.signout), name= 'signout'),
  ]
