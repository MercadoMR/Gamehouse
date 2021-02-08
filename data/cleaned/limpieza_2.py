"""
Este se encarga de unificar los dos conjuntos de datos en un mismo txt primero
Ademas separa los titulos, anios, companias, generos y plataformas en diferentes txts

splited[0] --> titulo
splited[1] --> compañia
splited[2] --> año
splited[3] --> genero
splited[4] --> plataforma
splited[5] --> descripcion
splited[6] --> imagen
splited[7] --> resto_del_texto

"""

def guardar_txt(datos,nombre): #Datos es una lista de strings
    txt = open(nombre, encoding = "utf-8", mode ="w") #a+
    for dato in datos:
        txt.write("\n"+dato)
    txt.close()


if __name__ == "__main__":
    """ Abrir el txt que tendra los juegos unificados y preparar datos por separado"""
    concentrado = open("unified/gameset.txt", encoding = "utf-8", mode="w")
    titulos = []
    companias = []
    anios = []
    generos = []
    plataformas = []
    """ El primer txt que tiene nuestros juegos """
    document_name = "cleaned/mobyset_cleaned.txt"
    document = open(document_name, encoding = "utf-8")
    games = document.read() #Take the document as a simple string
    document.close()
    while games != "":
        if(games == "\n"):
            break
        splited = games.split("|",7)
        games = splited [7]
        splited = splited[0:7]
        
        titulos.append(splited[0])
        companias.append(splited[1])
        anios.append(splited[2])
        generos.extend(splited[3].split(","))
        plataformas.extend(splited[4].split(","))

        
        splited = "|".join(splited) + "|"
        concentrado.write(splited)
    """ Limpiar repetidos """
    generos = list(set(generos))
    plataformas = list(set(plataformas))
    anios = list(set(anios))
    """ El segundo txt que tiene nuestros juegos """
    document_name = "cleaned/frenchset_cleaned.txt"
    document = open(document_name, encoding = "utf-8")
    games = document.read() #Take the document as a simple string
    document.close()
    while games != "":
        if(games == "\n"):
            break
        splited = games.split("|",7)
        games = splited [7]
        splited = splited[0:7]
        
        titulos.append(splited[0])
        companias.append(splited[1])
        anios.append(splited[2])
        generos.extend(splited[3].split(","))
        plataformas.extend(splited[4].split(","))
        
        splited = "|".join(splited) + "|"
        concentrado.write(splited)
    concentrado.close()
    """ Ultima limpieza y ordenamiento """
    titulos = sorted(titulos) #Guardar aunque haya repetidos
    #Guardar manual porque los datos ya tienen \n
    txt = open("unified/titulos.txt", encoding = "utf-8", mode ="w") #a+
    for titulo in titulos:
        txt.write(titulo)
    txt.close()
    companias = sorted(set(companias))
    guardar_txt(companias,"unified/companias.txt")
    anios = sorted(set(anios))
    guardar_txt(anios,"unified/anios.txt")
    generos = sorted(set(generos))
    guardar_txt(generos,"unified/generos.txt")
    plataformas = sorted(set(plataformas))
    guardar_txt(plataformas,"unified/plataformas.txt")   
    
        
        
        
        