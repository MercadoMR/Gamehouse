'''
Created on 20/12/2020

@author: mimr
'''
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404,HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from gamehouse.sjug.models import Jugador,Usuario,Juego,Imagen,CDE,Opinion,Recomendacion,Lista
from gamehouse.sjug.forms import UserForm,UsuarioForm,JugadorForm,MisGustosForm,CdeForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
import random
from gamehouse.sjug.models.jugador import JuegosFavoritos


""" Vistas de perfil """
def perfil(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        return render(request,'jugador/perfil.html',{'jugador':solicitado})     
    except Jugador.DoesNotExist:
        return redirect('error_404')

def opinion(request, jugador):
    solicitado = Jugador.objects.get(nickname = jugador)
    miOpinion=Opinion.objects.filter(jugador=jugador)
    paginator=Paginator(miOpinion,5)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    return render(request,'opinion.html',{'fOpinion':posts,'page':page,'jugador':solicitado})


#Por el momento sólo se puede cambiar el Usuario y no User ni Jugador
@login_required()
def editar_perfil(request,jugador):
    try:
        jugador = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != jugador.nickname:
            return redirect('error_403')    
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance = request.user)
            usuario_form = UsuarioForm(request.POST, instance = jugador.usuario)
            jugador_form = JugadorForm(request.POST, instance = jugador)
            if user_form.is_valid():
                usuario_form.save() #Por el momento solo actualiza usuario
                return redirect('/sjug/'+jugador.nickname+'/')
            else:
                return render(request,'jugador/editar_jugador.html',{'fusuario':usuario_form, 'fuser':user_form, 'fjugador':jugador_form})
        else:
            user_form = UserForm(instance = request.user)
            usuario_form = UsuarioForm(instance = jugador.usuario)
            jugador_form = JugadorForm(instance = jugador)
            return render(request,'jugador/editar_jugador.html',{'fusuario':usuario_form, 'fuser':user_form, 'fjugador':jugador_form})
    except Jugador.DoesNotExist:
        return redirect('error_404')

#Error al eliminar y querer registrarse de nuevo
@login_required()
def eliminar_perfil(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != solicitado.nickname:
            return redirect('error_403')
        try:
            usuario=get_object_or_404(Usuario,nombre=solicitado.usuario.nombre)
            userio=get_object_or_404(User,username=solicitado.nickname)
            jugo=get_object_or_404(Jugador,nickname=solicitado.nickname)
        except Exception:
            return HttpResponseNotFound('<h1>Page not found</h1>')   
        if request.method == 'POST':
            auth_logout(request)
            jugo.delete()
            usuario.delete()
            userio.delete()
            return redirect('index')
        else:
            return render(request,'jugador/eliminar_jugador.html')
    except Jugador.DoesNotExist:
        return redirect('error_404')

def gusto(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        return render(request,'jugador/gustos/gustos.html',{'jugador':solicitado})     
    except Jugador.DoesNotExist:
        return redirect('error_404')

#Doble submit, corregir
@login_required()
def mis_gustos(request,jugador):
    """ Mostrar formulario con Generos y Plataformas para su cambio """
    try:
        jugador = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != jugador.nickname:
            return redirect('error_403')    
        if request.method == 'POST':
            gustos_form = MisGustosForm(request.POST, instance=jugador)
            if gustos_form.is_valid():
                gustos_form.save()
                #return redirect('mis_gustos_2',id=id_gustos)
                return redirect('gusto',jugador = jugador.nickname)
        else:
            gustos_form = MisGustosForm(instance = jugador)
            return render(request,'jugador/gustos/mis_gustos.html',{'fgustos':gustos_form,'jugador':jugador})
    except Jugador.DoesNotExist:
        return redirect('error_404')

#Obtiene todos, limitar a cien y verificar funcionalidad 
@login_required()
def mis_juegos(request,jugador):
    """ Ver, añadir, o modificar mis juegos preferidos """
    try:
        jugador = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != jugador.nickname:
            return redirect('error_403')    
        juegos = Juego.objects.all()
        juegos = juegos[:15]
        favoritos = jugador.juegos.all()
        return render(request,'jugador/gustos/mis_juegos.html',{'juegos':juegos,'favoritos':favoritos,'jugador':jugador}) 
    except Jugador.DoesNotExist:
        return redirect('error_404')

@login_required()
def registro_palabras(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != solicitado.nickname:
            return redirect('error_403')
        #usuario=Usuario.objects.get(id=id)
        if request.method == 'POST':            
            cde_form = CdeForm(request.POST)
            if cde_form.is_valid():
                caracteristicas = cde_form.save(commit = False)
                caracteristicas.jugador = solicitado
                caracteristicas.save()
                return redirect('jugador',solicitado.nickname )
        else:
            cde_form = CdeForm()
            return render(request,'jugador/registro_palabras.html',{'fcde':cde_form})
        
    except Jugador.DoesNotExist:
        return redirect('error_404')
  

def mis_palabras(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != solicitado.nickname:
            return redirect('error_403')    
        try:
            #usuario=Usuario.objects.get(id_usuario=solicitado.usuario)
            carDE=get_object_or_404(CDE,jugador=solicitado)
        except Exception:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        if request.method == 'POST':            
            cde_form = CdeForm(request.POST,instance=carDE)
            if cde_form.is_valid():
                caracteristicas = cde_form.save(commit = False)
                caracteristicas.jugador = solicitado
                caracteristicas.save()      
                return redirect('mis_palabras',jugador=solicitado.nickname)  
        else:
            cde_form = CdeForm(instance=carDE)
            return render(request,'jugador/gustos/CDE.html',{'fcde':cde_form,'jugador':jugador})
    except Jugador.DoesNotExist:
        return redirect('error_404')  

#Accesible, pero aún con problemas, falta comprobar
@login_required()
def eliminar_mi_juego(request,jugador: str, id_juego: int):
    """ Eliminar un juego escogido """
    try:
        jugador = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != jugador.nickname:
            return redirect('error_403')
        try: 
            juego = Juego.objects.get(id_juego = id_juego)
            if request.method == 'POST':
                jugador.juegos.remove(juego)
                return redirect('mis_juegos',jugador = jugador.nickname)
            else:
                return render(request,'jugador/gustos/eliminar_mi_juego.html')
        except Juego.DoesNotExist:
            return redirect('error_404')    
    except Jugador.DoesNotExist:
        return redirect('error_404')
    
#Accesible, pero aún con problemas, falta comprobar
@login_required()
def agregar_mi_juego(request,jugador: str, id_juego: int):
    """ Agregar un juego escogido """
    try:
        jugador = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != jugador.nickname:
            return redirect('error_403')
        try: #Intentar recuperar jugador con ese juego
            juego = Juego.objects.get(id_juego = id_juego)
            if request.method == 'POST':
                jugador.juegos.add(juego)
                return redirect('mis_juegos',jugador = jugador.nickname)
            else:
                return render(request,'jugador/gustos/agregar_mi_juego.html')
        except Juego.DoesNotExist:
            return redirect('error_404')    
    except Jugador.DoesNotExist:
        return redirect('error_404')    

@login_required(login_url='/login')
def dashboard(request,jugador):
    try:
        jugador = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != jugador.nickname:
            return redirect('error_403')
        juegos = juegos_random()
        return render(request,'jugador/dashboard.html',{'juegos' : juegos})
    except Jugador.DoesNotExist:
        return redirect('error_404')

""" Funciones de opinion """

def mis_opiniones(request, jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != solicitado.nickname:
            return redirect('error_403')
        miOpinion=Opinion.objects.filter(jugador=solicitado.nickname)
        paginator=Paginator(miOpinion,5)
        page=request.GET.get('page')
        try:
            posts=paginator.page(page)
        except PageNotAnInteger:
            posts=paginator.page(1)
        except EmptyPage:
            posts=paginator.page(paginator.num_pages)
        return render(request,'jugador/opiniones.html',{'fOpinion':posts,'page':page})
    except Jugador.DoesNotExist:
        return redirect('error_404')

def recomendacion_puntuacion(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != solicitado.nickname:
            return redirect('error_403')
        return render(request,'jugador/recomendacion/Recomendacion_Puntuacion_General.html',{'jugador':solicitado})
    except Jugador.DoesNotExist:
        return redirect('error_404')

def recomendacion_puntuacion_gusto(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != solicitado.nickname:
            return redirect('error_403')
        juegos_favoritos= Opinion.objects.filter(gusto__gte=6).order_by('gusto')[:10]
        juegos=lista_puntuacion(juegos_favoritos)
        return render(request,'jugador/recomendacion/Recomendacion_Puntuacion.html',{'jugador':solicitado,'juegos_favoritos':juegos})
    except Jugador.DoesNotExist:
        return redirect('error_404')

def recomendacion_puntuacion_guion(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != solicitado.nickname:
            return redirect('error_403')
        juegos_favoritos= Opinion.objects.filter(guion__gte=6).order_by('guion')[:10]
        juegos=lista_puntuacion(juegos_favoritos)
        return render(request,'jugador/recomendacion/Recomendacion_Puntuacion.html',{'jugador':solicitado,'juegos_favoritos':juegos})
    except Jugador.DoesNotExist:
        return redirect('error_404')

def recomendacion_puntuacion_arte(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != solicitado.nickname:
            return redirect('error_403')
        juegos_favoritos= Opinion.objects.filter(artes__gte=6).order_by('artes')[:10]
        juegos=lista_puntuacion(juegos_favoritos)
        return render(request,'jugador/recomendacion/Recomendacion_Puntuacion.html',{'jugador':solicitado,'juegos_favoritos':juegos})
    except Jugador.DoesNotExist:
        return redirect('error_404')

def recomendacion_puntuacion_jugabilidad(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != solicitado.nickname:
            return redirect('error_403')
        juegos_favoritos= Opinion.objects.filter(jugabilidad__gte=6).order_by('jugabilidad')[:10]
        juegos=lista_puntuacion(juegos_favoritos)
        return render(request,'jugador/recomendacion/Recomendacion_Puntuacion.html',{'jugador':solicitado,'juegos_favoritos':juegos})
    except Jugador.DoesNotExist:
        return redirect('error_404')

def recomendacion_puntuacion_tecnico(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != solicitado.nickname:
            return redirect('error_403')
        juegos_favoritos= Opinion.objects.filter(tecnico__gte=6).order_by('tecnico')[:10]
        juegos=lista_puntuacion(juegos_favoritos)
        return render(request,'jugador/recomendacion/Recomendacion_Puntuacion.html',{'jugador':solicitado,'juegos_favoritos':juegos})
    except Jugador.DoesNotExist:
        return redirect('error_404')
#  Vistas para recomendacion 

def recomendacion(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != solicitado.nickname:
            return redirect('error_403')
        return render(request,'jugador/recomendacion/Recomendacion.html',{'jugador':solicitado})
    except Jugador.DoesNotExist:
        return redirect('error_404')

def recomendacion_descripcion(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != solicitado.nickname:
            return redirect('error_403')
        recomendacion = Recomendacion.objects.filter(jugador = solicitado, tipo = 'Descripción').first()
        listas = Lista.objects.filter(recomendacion = recomendacion)        
        paginator=Paginator(listas,10)
        page=request.GET.get('page')
        try:
            posts=paginator.page(page)
        except PageNotAnInteger:
            posts=paginator.page(1)
        except EmptyPage:
            posts=paginator.page(paginator.num_pages)

        return render(request,'jugador/recomendacion/Recomendacion_Descripcion.html',{'listas':posts,'page':page,})
    except Jugador.DoesNotExist:
        return redirect('error_404')

def recomendacion_genero(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != solicitado.nickname:
            return redirect('error_403')
        recomendacion = Recomendacion.objects.filter(jugador = solicitado, tipo = 'Genero').first()        
        listas = Lista.objects.filter(recomendacion = recomendacion)
        paginator=Paginator(listas,10)
        page=request.GET.get('page')
        try:
            posts=paginator.page(page)
        except PageNotAnInteger:
            posts=paginator.page(1)
        except EmptyPage:
            posts=paginator.page(paginator.num_pages)
        return render(request,'jugador/recomendacion/Recomendacion_Descripcion.html',{'listas':posts, 'page':page})
    except Jugador.DoesNotExist:
        return redirect('error_404')

def recomendacion_plataforma(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != solicitado.nickname:
            return redirect('error_403')
        recomendacion = Recomendacion.objects.filter(jugador = solicitado, tipo = 'Plataforma').first()
        listas = Lista.objects.filter(recomendacion = recomendacion)
        paginator=Paginator(listas,10)
        page=request.GET.get('page')
        try:
            posts=paginator.page(page)
        except PageNotAnInteger:
            posts=paginator.page(1)
        except EmptyPage:
            posts=paginator.page(paginator.num_pages)
        return render(request,'jugador/recomendacion/Recomendacion_Plataforma.html',{'listas':posts,'page':page})
    except Jugador.DoesNotExist:
        return redirect('error_404')

""" Vistas para recomendacion """
@login_required(login_url='/')
def tf_idf(request,jugador):
    return render(request,'jugador/recomendacion/tf_idf.html')


""" Funciones que no son puntos de URL """

def juegos_random():
    ##https://serpapi.com/images-results
    """ Esta funcion regresa pares juego, su imagen aleatorio """
    from django.core.exceptions import MultipleObjectsReturned
    disponibles = Juego.objects.all().count()  
    aleatorios = []
    for id_aleatorio in random.sample(range(0, disponibles), 12):
        juego = Juego.objects.get(id_juego = id_aleatorio)
        try:
            imagen = Imagen.objects.get(juego = id_aleatorio)
        except MultipleObjectsReturned:
            print("Excepcion generada:",MultipleObjectsReturned) 
            imagen = Imagen.objects.get(juego = id_aleatorio).first()[0]
        except Exception as e:
            print("Excepcion generada en inicio_jugador:",e)
            imagen = Imagen.objects.get(juego = 1)
        aleatorios.append((juego,imagen))
    return aleatorios

def lista_puntuacion(juegos_favoritos):
    ##https://serpapi.com/images-results
    """ Esta funcion regresa pares juego, su imagen aleatorio """
    from django.core.exceptions import MultipleObjectsReturned
    aleatorios = []
    for game in juegos_favoritos:
        juego = Juego.objects.get(titulo = game.juego)
        try:
            imagen = Imagen.objects.get(juego = game.juego)
        except MultipleObjectsReturned:
            print("Excepcion generada:",MultipleObjectsReturned) 
            imagen = Imagen.objects.get(juego = game.juego).first()[0]
        except Exception as e:
            print("Excepcion generada en inicio_jugador:",e)
            imagen = Imagen.objects.get(juego = 1)
        aleatorios.append((juego,imagen))
    return aleatorios