
"""
path('login/perfil/',include('gamehouse.sjug.urls')),
path('login/perfil/',include('gamehouse.sadm.urls')),

urlpatterns = [  
    path('mis_opiniones/<int:id>/',login_required(views.mis_opiniones), name='mis_opiniones'),  ### /sjug/<jugador>/opinion  Muestra lista de opiniones hechas por el jugador indicado
    path('eliminar/<int:id>/',login_required(views.eliminar), name='eliminar'), ### /sjug/<jugador>/eliminar
    path('',login_required(views.perfil_user), name='perfil_user'),  ### /sjug/<jugador> Ver perfil con opciones
    path('regresar_user/',login_required(views.regresar_user), name='regresar_user'), ### Borrar después mand inicio
    path('VVJuego/<int:id_juego>/<int:pk>/',login_required(views.VVJuego), name='VVJuego'), ### juegos/
    path('MiLista/<int:id>/',login_required(views.MiLista), name='MiLista'), ## Mis opniones cambiar a anterior
    path('caracteristicasDE/<int:id>/',login_required(views.caracteristicasDE), name='caracteristicasDE'),  ###   /sjug/<jugador>/gustos/CDE    
    path('InicioCDE/<int:id>/',login_required(views.InicioCDE), name='InicioCDE'), ### registro/CDE
    #path('prueba/',views.prueba,name="prueba"),  
    ###########################################################
    ###########################################################
    
    ###########################################################
    ###########################################################
    path('signout/',views.signout, name = 'signout'),
    path('Busqueda/',views.Busqueda, name = 'Busqueda'),
  ]

from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect,render,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.urls import reverse, reverse_lazy
from .models import *
from gamehouse.sadm.models import *
from .forms import UsuarioForm,JugadorForm,UserForm,GeneroForm,PlataformaForm,JuegoForm,OpinionForm,JuegosFavoritosForm,ImagenForm,CompaniaForm,MisGustosForm,CdeForm,CpuForm
from .filters import JuegoFilter

import random
from scipy import spatial
from django.core.exceptions import MultipleObjectsReturned
from _testcapi import exception_print



###############################################################################################
######################################USUARIO##################################################
###############################################################################################

  
def consolas(request):
  imagen =Imagen.objects.all()
  juego=Juego.objects.all()
  return render(request,'juegos/consolas.html',{'fImagen':imagen,'fJuego':juego})

def generos(request):
  imagen =Imagen.objects.all()
  juego=Juego.objects.all()
  return render(request,'juegos/generos.html',{'fImagen':imagen,'fJuego':juego})

def MiLista(request,id):
  MLista=JuegosFavoritos.objects.filter(jugador=id)
  myFilter=JuegoFilter(request.GET,queryset=MLista)
  MLista=myFilter.qs

  paginator=Paginator(MLista,10)
  page=request.GET.get('page')
  try:
    posts=paginator.page(page)
  except PageNotAnInteger:
    posts=paginator.page(1)
  except EmptyPage:
    posts=paginator.page(paginator.num_pages)
  return render(request,'jugador/milista.html',{'fMLista':posts,'page':page})

def CountGen(generos):
  genes=['Acción','Arcade','Aventura','Bélico','Carreras','Deporte','Disparo',
  'Educacional','Estrategia','Juegos de mesa','Música','Peleas','Plataforma',
  'Rol (RPG)','Rompecabezas','Simulación','Survival horror','Trivia']
  generos.sort()
  genes.sort()
  listgeneros=[]
  cero=0
  uno=1
  for i in range(18): 
    if genes[i] not in generos:
      listgeneros.append(cero)
    else:
      listgeneros.append(uno)
  #print("Esta son los generos",listgeneros)
  return listgeneros

def CountPlat(plataformas):
  platas=['Android','Arcade','Dreamcast','Gameboy',
  'Gameboy Advance','Gameboy Color','J2ME','Linux',
  'NES','Neo Geo','Nintendo 3DS','Nintendo 64','Nintendo DS',
  'Nintendo GameCube','Nintendo Switch','PS Vita','PSP',
  'PlayStation 1','PlayStation 2','PlayStation 3','PlayStation 4',
  'SNES','Wii','Wii U','Windows',
  'Xbox','Xbox 360','Xbox One','iOS']
  platas.sort()
  plataformas.sort()
  listplataformas=[]
  cero=0
  uno=1
  for i in range(29): 
    if platas[i] not in plataformas:
      listplataformas.append(cero)
    else:
      listplataformas.append(uno)
  return listplataformas

def Comparate(list1,list0):
  list2=list(list0)
  #use CountPlat or CountGen return list2
  result = 1 - spatial.distance.cosine(list1, list2)
  if result >= 0.5:
    return 1
  return 0

def agregar_vector(request):
  for video in Juego.objects.all():
    new=[]
    newps=[]
    genres=""
    platforms=""
    print(video.titulo)
    for gen in video.generos.all():
      new.append(gen.nombre)
    new=list(dict.fromkeys(new))#Delete duplicates
    new.sort()#Sort list
    new=CountGen(new)
    #genres=(",".join(new))
    genres=(','.join(str(x) for x in new))

    for pat in video.plataformas.all():
      newps.append(pat.nombre)
    newps=list(dict.fromkeys(newps))#Delete duplicates
    newps.sort()#Sort list
    newps=CountPlat(newps)
    platforms=(','.join(str(x) for x in newps))

    listbinario=ListGeneros()
    listbinario.juego=video
    listbinario.listgenero=genres
    listbinario.listplataforma=platforms
    listbinario.save()

  return render(request,'jugador/RecMiPalabra.html')


def RecMisPalabras(request,id):
  try:
    usuario=Usuario.objects.get(id=id)
    carCDE=get_object_or_404(Cde,cde=usuario)
    jugador=get_object_or_404(Jugador,cde=usuario)
    generos=GenerosFavoritos.objects.all().filter(jugador=usuario)
    plataforma=PlataformasFavoritas.objects.all().filter(jugador=usuario)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')
  
  if Recomendacion(obj):
    return render(request,'jugador/RecMiPalabra.html',{'RMPform':Recomendacion})
  else:
    print (generos.length())
    print (plataforma.length())
    #litgenes=CountGen(generos)
    #listplatas=CountPlat(plataformas)
    return render(request,'jugador/RecMiPalabra.html',{'RMPform':Recomendacion})


def Busqueda(request):
  search=""
  if request.method == 'GET':
    search=request.GET.get('search')
    VJuego=Juego.objects.all().filter(titulo__icontains=search)
    return render(request,'juegos/busqueda.html',{'fVJuego':VJuego})

def info_consolas(request):
  return render(request,'juegos/InfoConsolas.html')

def info_generos(request):
  return render(request,'juegos/InfoGeneros.html')


######################################################################
######################################################################
                        #CARACTERISTICAS#
######################################################################
######################################################################
def InicioCDE(request,id):
  usuario=Usuario.objects.get(id=id)
  if request.method == 'POST':            
    cde_form = CdeForm(request.POST)
    if cde_form.is_valid():
      caracteristicas = cde_form.save(commit = False)
      caracteristicas.cde = usuario
      caracteristicas.save()
      return redirect('iusuario')
  else:
    cde_form = CdeForm()
    return render(request,'jugador/CDE.html',{'fcde':cde_form})


def caracteristicasDE(request,id):
  try:
    usuario=Usuario.objects.get(id=id)
    carDE=get_object_or_404(Cde,cde=usuario)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  if request.method == 'POST':            
    cde_form = CdeForm(request.POST,instance=carDE)
    if cde_form.is_valid():
      caracteristicas = cde_form.save(commit = False)
      caracteristicas.cde = usuario
      caracteristicas.save()      
      return redirect('caracteristicasDE',id=id)    
  else:
    cde_form = CdeForm(instance=carDE)
    return render(request,'jugador/CDE.html',{'fcde':cde_form})


def ViewcaracteristicasPU(request):
  vcpu=Cpu.objects.all()
  paginator=Paginator(vcpu,5)
  page=request.GET.get('page')
  try:
    posts=paginator.page(page)
  except PageNotAnInteger:
    posts=paginator.page(1)
  except EmptyPage:
    posts=paginator.page(paginator.num_pages)
  return render(request,'adm/CaractPU.html',{'fvcpu':vcpu,'page':page})

def ViewcaracteristicasDE(request):
  vcde=Cde.objects.all()
  paginator=Paginator(vcde,5)
  page=request.GET.get('page')
  try:
    posts=paginator.page(page)
  except PageNotAnInteger:
    posts=paginator.page(1)
  except EmptyPage:
    posts=paginator.page(paginator.num_pages)
  return render(request,'adm/CaractDE.html',{'fvcde':vcde,'page':page})


def prueba(request,id):
    listdesc=[]
    listgames=[]
    listidf=[]
    list7=[]
    list8=[]
    list9=[]
    list10=[]

    ############    FILTER LIST
    usuario=Usuario.objects.get(id=id)
    jugador=Jugador.objects.get(usuario=usuario)
    setGames=Opinion.objects.all().filter(jugador=jugador.nickname,gusto__gte=6)

    ############    SEPARATE LIST
    for game in setGames:
      print("El juego es:",game)
      temp=[]
      suma=game.guion+game.artes+game.jugabilidad+game.tecnico
      print("La suma es:",suma)
      if game.gusto == 10:
        temp.append(game.juego)
        temp.append(suma)
        list10.append(temp)
      elif game.gusto == 9:
        temp.append(game.juego)
        temp.append(suma)
        list9.append(temp)
      elif game.gusto == 8:
        temp.append(game.juego)
        temp.append(suma)
        list8.append(temp)
      elif game.gusto == 7 or game.gusto == 6:
        temp.append(game.juego)
        temp.append(suma)
        list7.append(temp)

    ############    SORT LIST
    list10.sort(key=lambda x: x[1], reverse=True)
    list9.sort(key=lambda x: x[1], reverse=True)
    list8.sort(key=lambda x: x[1], reverse=True)
    list7.sort(key=lambda x: x[1], reverse=True)

    # for ele in list10:
    #   print("lista 10:",ele[0])

    ############    CHANGE LISTS IN LIST OF 10
    if len(list10)>0:
      if len(list10) >= 5:
        #listtemp=list(split(list10, 5)) #seccionar la lista
        listtemp = np.array_split(list10, 5)
        for evry in listtemp:
          listgames=random.sample(range(0, len(evry)), 1)
      else:#si no cumple con el ancho
        for elemento in list10:
          listgames.append(elemento)

    if len(list9)>0:
      limit=8-len(listgames)#Se resta 8 para saber los que faltan    
      if len(listgames)<5 and len(list9) >=3:#Agrega si en la lista no hay 5
        listtemp=np.array_split(list9,limit)#seccionar la lista
        for evry in listtemp:#de cada seccion obtiene un elemento
          listgames=random.sample(range(0, len(evry)), 1)
      elif len(list9) >=3:#Agrega 3
        listtemp=np.array_split(list9, 3)#seccionar la lista
        for evry in listtemp:#de cada seccion obtiene un elemento
          listgames=random.sample(range(0, len(evry)), 1)
      else:
        for elemento in list9:
          listgames.append(elemento)
    
    if len(list8)>0:
      limit=10-len(listgames)#Se resta 10 para saber los que faltan
      if len(listgames)<8 and len(list8) >=2:#Agrega si en la lista no hay 5
        listtemp=np.array_split(list8,limit)#seccionar la lista
        for evry in listtemp:#de cada seccion obtiene un elemento
          listgames=random.sample(range(0, len(evry)), 1)
      elif len(list8) >=2:
        listtemp=np.array_split(list8, 2)#seccionar la lista
        for evry in listtemp:#de cada seccion obtiene un elemento
          listgames=random.sample(range(0, len(evry)), 1)
      else:
        for elemento in list8:
          listgames.append(elemento)

    if len(list7)>0:
      limit=10-len(listgames)#Se resta 10 para saber los que faltan
      if len(listgames)<10 and len(list7) >=limit:
        listtemp=np.array_split(list7, limit)#seccionar la lista
        for evry in listtemp:#de cada seccion obtiene un elemento
          listgames=random.sample(range(0, len(evry)), 1)
      else:
        for elemento in list7:
          listgames.append(elemento)

    ############    CREATE LIST OF DESCRIPTION
    for ele in listgames:
      description=Juego.objects.filter(titulo=ele[0])
      for desc in description:
        listdesc.append(desc.descripcion)
    print("lista :",listdesc)
    
    for listtext in listdesc:
      listidf.append(idf(listtext))
    
    listidf.sort(reverse=True)

    


    return render(request,'prueba.html')







lg = [] #Lista de generos  
  aleatorios = []
  generos = []
  for favorito in GenerosFavoritos.objects.all():
    generos.append(favorito.genero)
    lg.append((Genero.objects.all().filter(nombre=favorito.genero))[0].id_genero)
  for id_genero in lg:
    print("Juegos para id_genero",id_genero)
    rs = GenerosAsociados.objects.all().filter(genero=id_genero)
    print("Que son ",len(rs))
    max_lim = 0
    if len(rs) < 20:
       max_lim = len(rs)
    else:
       max_lim = 20
    print("El maximo ",max_lim)
    randomList = random.sample(range(0, len(rs)), max_lim)
    print("La lista aleatoria:",randomList)
  
  # listjuegos=[]
  # for i in randomList:
    
  # for number in randomList:
  #    aleatorios.append()
  # for aleatorio in aleatorios:
  #   print(aleatorio)
  
  # print("Cadenas")

"""
