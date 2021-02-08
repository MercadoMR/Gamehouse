"""
Segundo script de inserción de datos en la 
base de datos gamehouse.db
Este paso de inserción depende de que ya estén insertados los datos
del paso anterior: Companias,Plataformas,Generos.
Formato de splited:

splited[0] --> titulo
splited[1] --> compañia
splited[2] --> año
splited[3] --> genero
splited[4] --> plataforma
splited[5] --> descripcion
splited[6] --> imagen
splited[7] --> resto_del_texto

"""
import sqlite3
from one_try import clean_description

def insert_database(datos,tabla):
    database_name = "gamehouse.db"
    query = "INSERT INTO sjug_"+tabla+" (nombre,descripcion) VALUES (?,?)"
    conn = sqlite3.connect(database_name)
    cr = conn.cursor()
    for dato in datos:
        #dato = dato.strip() ##Remove blank spaces
        dato = dato.replace("\n","") ##Remove new line characters
        cr.execute(query,(dato,"Descripción por defecto"))
    cr.close()
    conn.commit()
    conn.close()
    return

if __name__ == "__main__":
    database_name = "gamehouse.db"
    queries = [ "INSERT INTO sjug_juego (titulo,anio,descripcion,descripcion_limpia) VALUES (?,?,?,?)",
                 ###OBTENER ID DEL JUEGO
                 "SELECT id_juego FROM sjug_juego WHERE titulo = ?",#Obtener id_juego
                 ####### INSERTAR GENERO
                 "SELECT id_genero FROM sjug_genero WHERE nombre = ?",#Obtener id de cada genero que tiene el juego
                 "INSERT INTO sjug_GenerosAsociados (juego,genero) VALUES (?,?)", #Mandar ids
                 ####### INSERTAR PLATAFORMA
                 "SELECT id_plataforma FROM sjug_plataforma WHERE nombre = ?",
                 "INSERT INTO sjug_PlataformasAsociadas (juego,plataforma) VALUES (?,?)",
                 ########"INSERT INTO sjug_plataformas_asociadas (juego,plataforma) VALUES (?,?)",
                 ####### INSERTAR COMPANIA
                 "SELECT id_compania FROM sjug_compania WHERE nombre = ?",
                 "INSERT INTO sjug_CompaniasAsociadas (juego,compania) VALUES (?,?)",
                 ####### INSERTAR IMAGEN
                 "INSERT INTO sjug_imagen (referencia,alt,juego) VALUES (?,?,?)"
              ]
    """ Leer archivo que contiene todos los juegos """
    document_name = "mobyset.txt"
    document = open(document_name, encoding = "utf-8")
    games = document.read() 
    document.close()
    """ Conectar a la base de datos y obtener el cursor """
    conn = sqlite3.connect(database_name)
    cr = conn.cursor()
    while games != "":
        if(games == "\n"):
            break
        splited = games.split("|",7)
        games = splited[7]
        splited = splited[0:7]
        """ Limpiar titulo """
        splited[0] = splited[0].replace("\n","")
        """ Insertar juego """
        t = (splited[0],splited[2],splited[5],clean_description(splited[5])) #tit.,anio.,descrip.
        cr.execute(queries[0],t)
        """ Obtener id del juego insertado """
        cr.execute(queries[1],(splited[0],))
        id_juego = cr.fetchone()[0] #Returns a row
        print("\n\n********INSERTANDO JUEGO********\n\n")
        print("Id del juego:",id_juego)
        print("Juego:"+splited[0])
        """ Insertar los generos """
        print("\n----Insertando generos...")
        for genero in splited[3].split(","):
            cr.execute(queries[2],(genero,))
            id_genero = cr.fetchone()[0]
            t = (id_juego,id_genero)
            cr.execute(queries[3],t)
            print(genero+"("+str(id_genero)+") insertado!")
        """ Insertar las plataformas """
        print("\n----Insertando plataformas..")
        for plataforma in splited[4].split(","):
            cr.execute(queries[4],(plataforma,))
            id_plataforma = cr.fetchone()[0]
            t = (id_juego,id_plataforma)
            cr.execute(queries[5],t)
            print(plataforma+"("+str(id_plataforma)+") insertada!")
        """ Insertar las companias"""
        print("\n----Insertando compania...")
        cr.execute(queries[6],(splited[1],))
        id_compania = cr.fetchone()[0]
        t = (id_juego,id_compania)
        cr.execute(queries[7],t)
        print(splited[1]+"("+str(id_compania)+") insertada!")
        """ Insertar la imagen"""
        print("\n----Insertando imagen...")
        t = (splited[6],"Texto alternativo por defecto de la imagen del juego "+splited[0],id_juego)
        cr.execute(queries[8],t)
        print("Imagen:"+splited[6]+"\nde id_juego:"+str(id_juego)+" insertada!")
    cr.close()
    conn.commit()
    conn.close()
    







""" Viejas Queries """
"""
    queries = [ "INSERT INTO sjug_juego (titulo,descripcion,anio) VALUES (?,?,?)",
                 ###OBTENER ID DEL JUEGO
                 "SELECT id_juego FROM sjug_juego WHERE titulo = ?",#Obtener id_juego
                 ####### INSERTAR GENERO
                 "SELECT id_genero FROM sjug_genero WHERE nombre LIKE ?",#Obtener id de cada genero que tiene el juego
                 "INSERT INTO sjug_GenerosAsociados (juego,genero) VALUES (?,?)", #Mandar ids
                 ####### INSERTAR PLATAFORMA
                 "SELECT id_plataforma FROM sjug_plataforma WHERE nombre LIKE ?",
                 "INSERT INTO sjug_PlataformasAsociadas (juego,plataforma) VALUES (?,?)",
                 ########"INSERT INTO sjug_plataformas_asociadas (juego,plataforma) VALUES (?,?)",
                 ####### INSERTAR COMPANIA
                 "SELECT id_compania FROM sjug_compania WHERE nombre LIKE ?",
                 "INSERT INTO sjug_CompaniasAsociadas (juego,compania) VALUES (?,?)",
                 ####### INSERTAR IMAGEN
                 "INSERT INTO sjug_imagen (referencia,alt,juego) VALUES (?,?,?)"
              ]
"""
