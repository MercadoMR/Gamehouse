'''
Created on 20/12/2020

@author: mimr
'''
from django.shortcuts import render, get_object_or_404, redirect
from gamehouse.sjug.models import Jugador,Usuario,Juego,Imagen,Opinion
from gamehouse.sjug.forms import OpinionForm
from django.http import Http404
from gamehouse.sjug.views.jugador import juegos_random
from django.contrib.auth.decorators import login_required

def default(request):
    return render(request,'jugador/sjug.html')

"""  Vistas de interaccion jugador-juego """
#no hecha
def opiniones(request,jugador):
    return render(request,'pruebas/dashboard.html',{})
    
def busqueda(request):
  search=""
  if request.method == 'GET':
    search=request.GET.get('search')
    VJuego=Juego.objects.all().filter(titulo__icontains=search)
    return render(request,'juegos/busqueda.html',{'fVJuego':VJuego})


def juegos(request):
    juegos = juegos_random()    
    return render(request,'juegos/juegos.html',{'juegos':juegos})

def ver_juego(request,id_juego):
    try:
        juego = Juego.objects.get(id_juego = id_juego)
        imagen = Imagen.objects.get(juego = juego.id_juego)
        opiniones = juego.opiniones.all()
        contexto = {
                    'juego': juego,
                    'imagen': imagen,
                    'opiniones':opiniones
            }
        if request.method == 'POST':
            opinion_form = OpinionForm(request.POST)
            try:
                jugador = Jugador.objects.get(nickname = request.POST.get('jugador')) #Recibiendo campo oculto
                if opinion_form.is_valid():
                    opinion = opinion_form.save(commit = False)
                    opinion.comentario = request.POST.get('comentario')
                    opinion.jugador = jugador 
                    opinion.juego = juego
                    opinion.save()
                    print(opinion)
                    return redirect('ver_juego',id_juego=juego.id_juego)
            except Jugador.DoesNotExist:
                return redirect('error_404')
        else:
            opinion_form = OpinionForm()
            contexto['fopinion'] = opinion_form
            return render(request,'juegos/juego.html',contexto)
    except Juego.DoesNotExist:
        return redirect('error_404')
    except Imagen.DoesNotExist:
        return redirect('error_404')

@login_required()
def agregar_videojuego(request,jugador: str, id_juego: int):
    """ Agregar un juego escogido """
    print("El jugador es",jugador)
    try:
        usuario=Usuario.objects.get(id_usuario=jugador)
        jugador = Jugador.objects.get(usuario = usuario)
        if request.user.get_username() != jugador.nickname:
            return redirect('error_403')
        try: #Intentar recuperar jugador con ese juego
            juego = Juego.objects.get(id_juego = id_juego)
            if request.method == 'POST':
                jugador.juegos.add(juego)
                return redirect('ver_juego',id_juego = juego.id_juego)
            else:
                return render(request,'juegos/agregar_mi_juego.html',{'juego':juego})
        except Juego.DoesNotExist:
            return redirect('error_404')    
    except Jugador.DoesNotExist:
        return redirect('error_404') 

"""
def ver_juego(request,juego):
  #Juego = Juego.objects.get(id_juego = juego)
  #imagen = Imagen.objects.get(id_imagen = juego)
 
  if request.method == 'POST':
    opinion_form = OpinionForm(request.POST)
    if opinion_form.is_valid():
      rOpinion=opinion_form.save(commit = False)
      rOpinion.juego=Juego.objects.get(id_juego=id_juego)##############corregir con Jugador
      rOpinion.jugador=Jugador.objects.get(usuario=pk)##################corregir con Jugador
      rOpinion.gusto=request.POST.get('gusto')
      rOpinion.guion=request.POST.get('guion')
      rOpinion.artes=request.POST.get('artes')
      rOpinion.jugabilidad=request.POST.get('jugabilidad')
      rOpinion.tecnico=request.POST.get('tecnico')
      rOpinion.save()
      return redirect('VVJuego',id_juego=id_juego,pk=pk)
      #return redirect('regresar_user')
  else:
  
  opinion_form = OpinionForm()
  VJuego = Juego.objects.get(id_juego=juego)
  imagen = Imagen.objects.get(id_imagen=juego)    
  return render(request,'juegos/juego.html',{'fopinion':opinion_form,'VJuego':VJuego,'fimagen':imagen})
  """
