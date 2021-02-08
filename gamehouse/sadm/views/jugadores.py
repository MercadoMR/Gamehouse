from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect,render,get_object_or_404
from gamehouse.sjug.models import *
from gamehouse.sjug.forms import UsuarioForm,JugadorForm,UserForm
from gamehouse.sjug.filters import JuegoFilter
from gamehouse.sadm.models import Administrador

def gestion_usuarios(request,administrador):
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        jugador = Jugador.objects.get(usuario = solicitado.usuario)
        if request.user.get_username() == jugador.nickname: 
            dataset = Usuario.objects.exclude(nombre__icontains=administrador)
            paginator=Paginator(dataset,2)
            page=request.GET.get('page')
            try:
                posts=paginator.page(page)
            except PageNotAnInteger:
                posts=paginator.page(1)
            except EmptyPage:
                posts=paginator.page(paginator.num_pages)
            
            return render(request,'adm/jugadores/gestion_usuario.html',{'dataset':posts,'page':page,'administrador':solicitado})
                
        else:
            print("No tienes permisos!!")
            raise PermissionDenied            
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")

def registro_usuarios(request,administrador):
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        jugador = Jugador.objects.get(usuario = solicitado.usuario)
        if request.user.get_username() == jugador.nickname: 
            if request.method == 'POST':
                user_form = UserForm(request.POST) 
                usuario_form = UsuarioForm(request.POST)
                jugador_form = JugadorForm(request.POST)
            
                if all([usuario_form.is_valid(),jugador_form.is_valid(),user_form.is_valid()]):
                    usuario = usuario_form.save()
                    jugador = jugador_form.save(commit = False)
                    jugador.id_jugador = usuario
                    jugador.save()
                    user_form.save()
                    username = user_form.cleaned_data['username']
                    password = user_form.cleaned_data['password1']
                    user = authenticate(username = username,password = password)
                    login(request, user)
                    return redirect('gestion_usuarios',administrador=administrador)
            else:
                user_form=UserForm()
                usuario_form = UsuarioForm()
                jugador_form = JugadorForm()
            return render(request,'adm/jugadores/registro_jugadores.html',{'fusuario':usuario_form, 'fuser':user_form, 'fjugador':jugador_form,'administrador':solicitado})    
                
        else:
            print("No tienes permisos!!")
            raise PermissionDenied            
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")

def editar_usuarios(request,administrador,id_usuario):
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        jugador = Jugador.objects.get(usuario = solicitado.usuario)
        if request.user.get_username() == jugador.nickname: 
            try:    
                usuario=get_object_or_404(Usuario,id_usuario=id_usuario)
                userio=get_object_or_404(User,username=one.nickname)
                jugador=get_object_or_404(Jugador,nickname=one.nickname)
            except Exception:
                return HttpResponseNotFound('<h1>Page not found</h1>')

            if request.method == 'POST':
                usuario_form = UsuarioForm(request.POST, instance=usuario)
                jugador_form = JugadorForm(request.POST, instance=jugador)
                if usuario_form.is_valid():
                    usuario = usuario_form.save()
                    jugador=jugador_form.save()
                    return redirect('gestion_usuarios',administrador=administrador)
            else:
                usuario_form = UsuarioForm(instance=usuario)
                jugador_form = JugadorForm(instance=usuario)
            return render(request,'adm/jugadores/editar_jugadores.html',{'fusuario':usuario_form,'fjugador':jugador_form,'administrador':solicitado})
                
        else:
            print("No tienes permisos!!")
            raise PermissionDenied            
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")

def eliminar_usuarios(request,administrador,id_usuario):
    print("usuario id",id_usuario)
    print("usuario",administrador)
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        jugador = Jugador.objects.get(usuario = solicitado.usuario)
        if request.user.get_username() == jugador.nickname: 
            try:
                usuario=get_object_or_404(Usuario,id_usuario=id_usuario)
                userio=get_object_or_404(User,username=one.nickname)
                jugador=get_object_or_404(Jugador,nickname=one.nickname)
            except Exception:
                return HttpResponseNotFound('<h1>Page not found</h1>')

            if request.method=="POST":
                jugador.delete()
                userio.delete()
                usuario.delete()
                return redirect('gestion_usuarios',administrador=administrador)
            else:
                return render(request,'adm/jugadores/eliminar_jugadores.html',{'administrador':solicitado})
        else:
            print("No tienes permisos!!")
            raise PermissionDenied         
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")