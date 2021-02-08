from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect,render,get_object_or_404
from gamehouse.sjug.models import *
from gamehouse.sjug.forms import GeneroForm,PlataformaForm,JuegoForm,ImagenForm,CompaniaForm
from gamehouse.sjug.filters import JuegoFilter
from gamehouse.sadm.models import Administrador


def lista_videojuegos(request,administrador):
      try:
        solicitado = Administrador.objects.get(nombre = administrador)
        jugador = Jugador.objects.get(usuario = solicitado.usuario)
        if request.user.get_username() == jugador.nickname: ## Tengo iniciada una sesión de adm
            juegos = Juego.objects.all() 
            myFilter=JuegoFilter(request.GET,queryset=juegos)
            juegos=myFilter.qs

            paginator=Paginator(juegos,10)
            page=request.GET.get('page')
            try:
              posts=paginator.page(page)
            except PageNotAnInteger:
              posts=paginator.page(1)
            except EmptyPage:
              posts=paginator.page(paginator.num_pages)   
            return render(request,'adm/juegos/videojuegos.html',{'juegos':posts,'myFilter':myFilter,'page':page,'administrador':solicitado})    
        else:# Tengo iniciada sesión como jugador normal
            print("No tienes permisos!!")
            raise PermissionDenied # Error 403 forbidden             
      except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")

def editar_videojuegos(request,administrador,id_juego):
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        jugador = Jugador.objects.get(usuario = solicitado.usuario)
        if request.user.get_username() == jugador.nickname: ## Tengo iniciada una sesión de adm
          try:    
            vjuego=get_object_or_404(Juego,id_juego=id_juego)
            vimagen=get_object_or_404(Imagen,id_imagen=id_juego)
          except Exception:
            return HttpResponseNotFound('<h1>Page not found</h1>')

          if request.method == 'POST':
            vjuego_form = JuegoForm(request.POST, instance=vjuego)
            imagen_form = ImagenForm(request.POST, instance=vimagen)
            if all([vjuego_form.is_valid(),imagen_form.is_valid()]):      
              imagen_form.save()
              vjuego_form.save()
              return redirect('lista_videojuegos',administrador=administrador)
          else:
            imagen_form = ImagenForm(instance=vimagen)
            vjuego_form = JuegoForm(instance=vjuego)
            return render(request,'adm/juegos/editar_videojuego.html',{'VJuegos':vjuego_form,'fImagen':imagen_form,'administrador':solicitado})
        else:# Tengo iniciada sesión como jugador normal
            print("No tienes permisos!!")
            raise PermissionDenied # Error 403 forbidden             
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")

def eliminar_videojuegos(request,administrador,id_juego):
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        jugador = Jugador.objects.get(usuario = solicitado.usuario)
        if request.user.get_username() == jugador.nickname: ## Tengo iniciada una sesión de adm
          try:
            vjuego=get_object_or_404(Juego,id_juego =id_juego)
            vimagen=get_object_or_404(Imagen,id_imagen=id_juego)

            # vgenero=get_object_or_404(  Genero,id = id)
            # vplataforma=get_object_or_404(Plataforma, id=id)
          except Exception:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        
          if request.method=="POST":
            # vgenero.delete()
            # vplataforma.delete()
            vimagen.delete()
            vjuego.delete()
            return redirect('lista_videojuegos',administrador=administrador)
          else:
            return render(request,'adm/juegos/eliminar_videojuegos.html',{'administrador':solicitado}) 
                
        else:# Tengo iniciada sesión como jugador normal
            print("No tienes permisos!!")
            raise PermissionDenied # Error 403 forbidden             
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")

def registro_videojuegos(request,administrador):
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        jugador = Jugador.objects.get(usuario = solicitado.usuario)
        if request.user.get_username() == jugador.nickname: ## Tengo iniciada una sesión de adm
            if request.method == 'POST':         
              juego_form = JuegoForm(request.POST)
              imagen_form = ImagenForm(request.POST)
              # compania_form = CompaniaForm(request.POST)
              if all([juego_form.is_valid(),imagen_form.is_valid()]):      
                imagen_form.save()
                juego_form.save()
                return redirect('lista_videojuegos',administrador=administrador)
            else:
              juego_form=JuegoForm()
              imagen_form = ImagenForm()
            return render(request,'adm/juegos/registro_videojuego.html',{'VJuegos':juego_form,'fImagen':imagen_form,'administrador':solicitado})
                
        else:# Tengo iniciada sesión como jugador normal
            print("No tienes permisos!!")
            raise PermissionDenied # Error 403 forbidden             
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")

def genero_plataforma(request,administrador):
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        jugador = Jugador.objects.get(usuario = solicitado.usuario)
        if request.user.get_username() == jugador.nickname: ## Tengo iniciada una sesión de adm
            plataforma=Plataforma.objects.all()
            genero=Genero.objects.all()
            return render(request,'adm/juegos/generos_plataformas.html',{'fgenero':genero,'fplataforma':plataforma,'administrador':solicitado})                
        else:# Tengo iniciada sesión como jugador normal
            print("No tienes permisos!!")
            raise PermissionDenied # Error 403 forbidden             
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")

def registro_gen_pla(request,administrador):
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        jugador = Jugador.objects.get(usuario = solicitado.usuario)
        if request.user.get_username() == jugador.nickname: ## Tengo iniciada una sesión de adm
          if request.method == 'POST':
            genero_form = GeneroForm(request.POST)
            plataforma_form = PlataformaForm(request.POST)
            if all([genero_form.is_valid(),plataforma_form.is_valid()]):
              genero_form.save()
              plataforma_form.save()
              return redirect('genero_plataforma',administrador=administrador)
          else:
            genero_form = GeneroForm()
            plataforma_form = PlataformaForm()
          return render(request,'adm/juegos/registro_Gen_Pla.html',{'fgenero':genero_form, 'fplataforma':plataforma_form,'administrador':solicitado})
                
        else:# Tengo iniciada sesión como jugador normal
            print("No tienes permisos!!")
            raise PermissionDenied # Error 403 forbidden             
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")

def eliminar_Plataforma(request,administrador,id_plataforma):
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        jugador = Jugador.objects.get(usuario = solicitado.usuario)
        if request.user.get_username() == jugador.nickname: ## Tengo iniciada una sesión de adm
            try:
              usuario=get_object_or_404(Plataforma,id_plataforma=id_plataforma)
            except Exception:
              return HttpResponseNotFound('<h1>Page not found</h1>')

            if request.method=="POST":
              usuario.delete()
              return redirect('genero_plataforma',administrador=administrador)
            else:
              return render(request,'adm/juegos/eliminar_Plataforma.html',{'administrador':solicitado})
                
        else:# Tengo iniciada sesión como jugador normal
            print("No tienes permisos!!")
            raise PermissionDenied # Error 403 forbidden             
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")

def editar_Plataforma(request,administrador,id_plataforma):
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        jugador = Jugador.objects.get(usuario = solicitado.usuario)
        if request.user.get_username() == jugador.nickname: ## Tengo iniciada una sesión de adm
          try:    
            usuario=get_object_or_404(Plataforma,id_plataforma=id_plataforma)
          except Exception:
            return HttpResponseNotFound('<h1>Page not found</h1>')

          if request.method == 'POST':
            usuario_form = PlataformaForm(request.POST, instance=usuario)
            if usuario_form.is_valid():
              usuario_form.save()
              return redirect('genero_plataforma',administrador=administrador)
          else:
            usuario_form = PlataformaForm(instance=usuario)
          return render(request,'adm/juegos/editar_Plataforma.html',{'fplataforma':usuario_form,'administrador':solicitado})
                
        else:# Tengo iniciada sesión como jugador normal
            print("No tienes permisos!!")
            raise PermissionDenied # Error 403 forbidden             
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")

def eliminar_Genero(request,administrador,id_genero):
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        jugador = Jugador.objects.get(usuario = solicitado.usuario)
        if request.user.get_username() == jugador.nickname: ## Tengo iniciada una sesión de adm
            try:
              usuario=get_object_or_404(Genero,id_genero=id_genero)
            except Exception:
              return HttpResponseNotFound('<h1>Page not found</h1>')

            if request.method=="POST":
              usuario.delete()
              return redirect('genero_plataforma',administrador=administrador)
            else:
              return render(request,'adm/juegos/eliminar_Genero.html',{'administrador':solicitado})
                
        else:# Tengo iniciada sesión como jugador normal
            print("No tienes permisos!!")
            raise PermissionDenied # Error 403 forbidden             
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")

def editar_Genero(request,administrador,id_genero):
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        jugador = Jugador.objects.get(usuario = solicitado.usuario)
        if request.user.get_username() == jugador.nickname: ## Tengo iniciada una sesión de adm
          try:    
            genero=get_object_or_404(Genero,id_genero=id_genero)
          except Exception:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        
          if request.method == 'POST':
            genero_form = GeneroForm(request.POST, instance=genero)
            if genero_form.is_valid():
              genero_form.save()
              return redirect('genero_plataforma',administrador=administrador)
          else:
            genero_form = GeneroForm(instance=genero)
          return render(request,'adm/juegos/editar_Genero.html',{'fgenero':genero_form,'administrador':solicitado})
                
        else:# Tengo iniciada sesión como jugador normal
            print("No tienes permisos!!")
            raise PermissionDenied # Error 403 forbidden             
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")

def ViewcaracteristicasPU(request,administrador):
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        jugador = Jugador.objects.get(usuario = solicitado.usuario)
        if request.user.get_username() == jugador.nickname: ## Tengo iniciada una sesión de adm
            vcpu=CPU.objects.all()
            paginator=Paginator(vcpu,5)
            page=request.GET.get('page')
            try:
              posts=paginator.page(page)
            except PageNotAnInteger:
              posts=paginator.page(1)
            except EmptyPage:
              posts=paginator.page(paginator.num_pages)
            return render(request,'adm/juegos/CaractPU.html',{'fvcpu':vcpu,'page':page,'administrador':solicitado})
                
        else:# Tengo iniciada sesión como jugador normal
            print("No tienes permisos!!")
            raise PermissionDenied # Error 403 forbidden             
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")

def ViewcaracteristicasDE(request,administrador):
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        jugador = Jugador.objects.get(usuario = solicitado.usuario)
        if request.user.get_username() == jugador.nickname: ## Tengo iniciada una sesión de adm
          vcde=CDE.objects.all()
          paginator=Paginator(vcde,5)
          page=request.GET.get('page')
          try:
            posts=paginator.page(page)
          except PageNotAnInteger:
            posts=paginator.page(1)
          except EmptyPage:
            posts=paginator.page(paginator.num_pages)
          return render(request,'adm/juegos/CaractDE.html',{'fvcde':vcde,'page':page,'administrador':solicitado})
                
        else:# Tengo iniciada sesión como jugador normal
            print("No tienes permisos!!")
            raise PermissionDenied # Error 403 forbidden             
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")