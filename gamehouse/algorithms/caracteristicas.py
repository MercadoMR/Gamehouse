#https://medium.com/@wenxuan0923/feature-extraction-from-text-using-countvectorizer-tfidfvectorizer-9f74f38f86cc
import nltk
import random
from gamehouse.sjug.models import Juego,Vector_Caracteristicas,ListGeneros
from gamehouse.algorithms.tf_idf import similitud_coseno

def calcular_cpus(juegos):
    """ Esta funcion recibe la lista de ids de los juegos """
    seccion = len(juegos) // 5
    cpus = []
    terminos = {
            0:4, #Obtener los tres primeros terminos de la primera seccion
            1:3, #Obtener los dos siguients terminos de la segunda seccion
            2:2, #Obtener los dos siguients terminos de la tercera seccion
            3:1,
            4:1,
            5:0
    }
    #Caso donde hay resto:
    if  len(juegos) % 5: # Si hay resto hacer lista con juegos restantes
        terminos = {
            0:3, #Obtener los tres primeros terminos de la primera seccion
            1:2, #Obtener los dos siguients terminos de la segunda seccion
            2:2, #Obtener los dos siguients terminos de la tercera seccion
            3:1,
            4:1,
            5:1
        }
    i = 0
    while i < 5: #Obtener listas de juegos por secciones
        inicio = i * seccion
        chunk = juegos[inicio:inicio+seccion]
        escogido = random.randint(0, seccion-1) #Escoger un indice aleatorio entre 0 y el tamanio de la lista
        juego = Juego.objects.get( id_juego = chunk[escogido] )
        tokens = nltk.word_tokenize(juego.descripcion_limpia,"spanish")
        tokens_dist = nltk.FreqDist(tokens)
        for word, frequency in tokens_dist.most_common(terminos[i]):
            cpus.append(word)
            print('%s;%d' % (word, frequency))
        i = i + 1
    if len(juegos) % 5: #Si hay resto hacer para una ultima lista
        inicio = i * seccion ## Obtener una lista con el sobrante
        resto = juegos[inicio:]
        escogido = random.randint(0, seccion-1) #Escoger un indice aleatorio entre 0 y el tamanio de la lista
        juego = Juego.objects.get( id_juego = resto[escogido] )
        tokens = nltk.word_tokenize(juego.descripcion_limpia,"spanish")
        tokens_dist = nltk.FreqDist(tokens)
        for word, frequency in tokens_dist.most_common(terminos[i]):
            cpus.append(word)
            print('%s;%d' % (word, frequency))
    return cpus

def calcular_caracteristicas(caracteristicas,frecuencia):
    cpus=""
    listtemp=[]    
    for cde in caracteristicas:
        listtemp.append(frecuencia[cde])
    cpus=','.join(str(x) for x in listtemp)
    return cpus

def change_str(vector_car):
    cpus=','.join(str(x) for x in listtemp)
    return cpus

import numpy as np
def calcular_vec_usuario(juegos,gamer):
    perfil_usuario=[]
    listgeneros=[]
    listplataformas=[]
    listcpu=[]
    listcdes=[]
    i=0
    for game in  juegos:
        print("Juego",game)
        Gen_Pla=ListGeneros.objects.get(juego=game)
        vector = Vector_Caracteristicas.objects.filter(jugador=gamer,juego=game)
        #print("Genero",Gen_Pla.juego)
        for vec in vector:
          print("Vec",vec.juego)
          cpus = vec.cpus
          cdes = vec.cdes
          cpus = cpus.split(',')
          cdes = cdes.split(',')
          
          listcpu.append(cpus)
          listcdes.append(cdes)
        #Get elements from every game of user
        genes=Gen_Pla.listgenero
        platas=Gen_Pla.listplataforma
        #Get a list of elements
        platas=platas.split(',')
        genes=genes.split(',')
        #append in one list
        listgeneros.append(genes)
        listplataformas.append(platas)


    #https://stackoverflow.com/questions/29661574/normalize-numpy-array-columns-in-python
    #Change type to Array
    gen = np.array(listgeneros).astype(np.float)
    pla = np.array(listplataformas).astype(np.float)
    ccpu = np.array(listcpu).astype(np.float)
    ccde = np.array(listcdes).astype(np.float)
    #Normalize
    gen = gen / gen.max(axis=0)
    pla = pla / pla.max(axis=0)
    ccpu = ccpu / ccpu.max(axis=0)
    ccde = ccde / ccde.max(axis=0)
    #Avoid division by zero
    gen[np.isnan(gen) | np.isinf(gen)] = 0
    pla[np.isnan(pla) | np.isinf(pla)] = 0
    ccpu[np.isnan(ccpu) | np.isinf(ccpu)] = 0
    ccde[np.isnan(ccde) | np.isinf(ccde)] = 0
    
    #Calculate de Mean
    #Sort   Genero,Plataforma,CPU,CDE
    gen = np.average(gen, axis=0)
    pla = np.average(pla, axis=0)
    ccpu = np.average(ccpu, axis=0)
    ccde = np.average(ccde, axis=0)
    vector_perfil = np.concatenate([gen,
                                    pla,
                                    ccpu,
                                    ccde
                                    ])
    vector_perfil = [ str(number) for number in vector_perfil]
    print(vector_perfil)
    vector_perfil = ','.join(vector_perfil)
    return vector_perfil


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

def obtener_vector(gamer,juego):
    gen_plat= ListGeneros.objects.get(juego = juego) 
    vector = gen_plat.listgenero + gen_plat.listplataforma
    vector = vector.split(",")
    obtenido = Vector_Caracteristicas.objects.get(jugador = gamer,juego = juego)
    return 
    
def recomendacion_genero(jugador,genero):
    vectores = Vector_Caracteristicas.objects.filter(jugador = jugador) 
    lista_genero = []
    print("Filtrando para el genero:",genero)
    print("Todos:",len(vectores))
    vector_perfil = (jugador.vector_perfil).split(',')
    vector_perfil = np.array(vector_perfil).astype(np.float)
    for vector in vectores:
        if genero in vector.juego.generos.all():
            vector_videojuego = ListGeneros.objects.get(juego = vector.juego)
            vector_videojuego = vector_videojuego.listgenero + ',' + vector_videojuego.listplataforma
            vector_videojuego = vector_videojuego + ',' + vector.cpus + ','+ vector.cdes
            vector_videojuego = vector_videojuego.split(',') 
            vector_videojuego = np.array(vector_videojuego).astype(np.float)
            similitud = similitud_coseno(vector_perfil,vector_videojuego)
            lista_genero.append( (vector.juego,similitud) )
    lista_genero = list(set(lista_genero))
    lista_genero.sort(key=lambda x: x[1], reverse=True)
    lista_genero = lista_genero[:15]
    recomendacion = []
    for pair in lista_genero:
        recomendacion.append(pair[0])
    return recomendacion

def recomendacion_plataforma(jugador,plataforma):
    vectores = Vector_Caracteristicas.objects.filter(jugador = jugador) 
    lista_plataforma = []
    print("Filtrando para la plataforma:",plataforma)
    print("Todos:",len(vectores))
    vector_perfil = (jugador.vector_perfil).split(',')
    vector_perfil = np.array(vector_perfil).astype(np.float)
    for vector in vectores:
        if plataforma in vector.juego.plataformas.all():
            vector_videojuego = ListGeneros.objects.get(juego = vector.juego)
            vector_videojuego = vector_videojuego.listgenero + ',' + vector_videojuego.listplataforma
            vector_videojuego = vector_videojuego + ',' + vector.cpus + ','+ vector.cdes
            vector_videojuego = vector_videojuego.split(',') 
            vector_videojuego = np.array(vector_videojuego).astype(np.float)
            similitud = similitud_coseno(vector_perfil,vector_videojuego)
            lista_plataforma.append( (vector.juego,similitud) )
    lista_plataforma= list(set(lista_plataforma))
    lista_plataforma.sort(key=lambda x: x[1], reverse=True)
    lista_plataforma = lista_plataforma[:15]
    recomendacion = []
    for pair in lista_plataforma:
        recomendacion.append(pair[0])
    return recomendacion

    """
    0.2,0.1,0.333
    -> cpu0,cpu1,
    -> 30, 20 , 1,2,0,
    for genero in generos:
        juegos = []
        numero_juegos = genero.juego_set.all().count()
        muestreo = 20
        if numero_juegos < 20:
            muestreo = numero_juegos
        randomList = random.sample(range(0, numero_juegos), muestreo)
        for indice in randomList:
            juegos.append(genero.juego_set.all()[indice])
        for juego in juegos:
            vector_juego = obtener_vector(gamer,juego)
            
            ruta = Tf_Idf.objects.get(juego = juego)
            dt = open(ruta.vector, 'rb')
            vector_juego = load(dt)
            dt.close()
            similitud = similitud_coseno(vector_favorito, vector_juego)
            juego_puntaje.append( (juego,similitud) )
    juego_puntaje.sort(key=lambda x: x[1], reverse=True)
    juego_imagen = []
    for par in juego_puntaje:
        tupla = (par[0],Imagen.objects.get(juego = par[0]))
        juego_imagen.append(tupla)
   
    return juego_imagen
    """

