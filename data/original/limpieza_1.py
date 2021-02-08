"""
Leer como cadena todo el txt de datos.
Separar cada juego utilizando split("|",7) que devuelve una lista de ocho elementos:
[titulo,compañia,año,genero,plataforma,descripcion,imagen, resto_del_texto]

Debido a los saltos de línea para hacer más legible el txt, el titulo de cada juego tiene
un salto de linea antes de la cadena, de la forma \nResto del texto.
Por ejemplo: \nMetal Slug 1
Así que hay que limpiar cuando se quiera insertar en la db utilizando: splited[0].replace("\n","")

splited[0] --> titulo
splited[1] --> compañia
splited[2] --> año
splited[3] --> genero
splited[4] --> plataforma
splited[5] --> descripcion
splited[6] --> imagen
splited[7] --> resto_del_texto

Correr dos veces, la primera document_name es mobyset.txt, la segunda frenchset.txt
"""

def guardar_txt(datos,nombre): #Datos es una lista de strings
    txt = open(nombre, encoding = "utf-8", mode ="a+")
    for dato in datos:
        txt.write(dato)
    txt.close()


if __name__ == "__main__":
    document_name = "original/frenchset.txt"
    document = open(document_name, encoding = "utf-8")
    games = document.read() #Take the document as a simple string
    document.close()
    resultado = open("cleaned/frenchset_cleaned.txt", encoding = "utf-8", mode="w")
    while games != "":
        if(games == "\n"):
            break
        splited = games.split("|",7)
        games = splited [7]
        splited = splited[0:7]
        """ Limpiar espacios extras """
        if splited[5][0] == '\"':
            splited[5] = splited[5][1:]
        if splited[5][-1] == '\"':
            splited[5] = splited[5][:-1]
        splited[5] = splited[5].strip()
        """ Limpieza de generos """
        generos = splited[3].split(",") # Crear una lista con los datos entre cada coma
        generos = [genero for genero in generos if genero] ## Remove empty elem.
        generos = ",".join(generos) # Regresar a representación de string
        """ Limpieza de plataformas """
        plataformas = splited[4].split(",")
        plataformas = [plataforma for plataforma in plataformas if plataforma]
        plataformas = ",".join(plataformas) 
        """ Escritura de limpio """
        splited[3] = generos
        splited[4] = plataformas
        print(splited) 
        print("\n\n")
        splited = "|".join(splited) + "|"
        resultado.write(splited)
    resultado.close()   
        
        
        
        
