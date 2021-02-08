from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect,render,get_object_or_404
from gamehouse.sjug.models import *
#from .forms import Administrador
from gamehouse.sadm.models import Administrador
from gamehouse.sjug.filters import JuegoFilter
from django.contrib.auth import logout

def perfil_adm(request,administrador):
    try:
        print(administrador)
        solicitado = Administrador.objects.get(nombre = administrador)       
        return render(request,'adm/perfil_adm.html',{'administrador':solicitado})                
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")

def signout(request,administrador):
    admin = Administrador.objects.get(nombre = administrador)
    jugador = Jugador.objects.get(usuario = admin.usuario)
    logout(request)
    return redirect('index')