"""
Primer script de inserción de datos en la 
base de datos gamehouse_limpia.db
Se insertan los datos que no dependen de ningún otro.
Companias,Plataformas,Generos
"""
import sqlite3

def insert_database(datos,tabla):
    database_name = "gamehouse.db"
    query = "INSERT INTO sjug_"+tabla+" (nombre,descripcion) VALUES (?,?)"
    conn = sqlite3.connect(database_name)
    cr = conn.cursor()
    for dato in datos:
        #dato = dato.strip() ##Remove blank spaces
        dato = dato.replace("\n","") ##Remove new line characters
        cr.execute(query,(dato,"Descripción por defecto de "+dato))
    cr.close()
    conn.commit()
    conn.close()
    return

if __name__ == "__main__":
    queries = [ "INSERT INTO sjug_genero (nombre,descripcion) VALUES (?,?)",
                "INSERT INTO sjug_compania (nombre,descripcion) VALUES(?,?)",
                "INSERT INTO sjug_plataforma (nombre,descripcion) VALUES(?,?)"]
    """ INSERTAR COMPANIAS """
    document_name = "standalone/companias.txt"
    document = open(document_name, encoding = "utf-8")
    lineas= document.readlines() 
    document.close()
    insert_database(lineas, "compania")
    """ INSERTAR GENEROS """
    document_name = "standalone/generos.txt"
    document = open(document_name, encoding = "utf-8")
    lineas= document.readlines() 
    document.close()
    insert_database(lineas, "genero")
    """ INSERTAR PLATAFORMAS """
    document_name = "standalone/plataformas.txt"
    document = open(document_name, encoding = "utf-8")
    lineas= document.readlines() 
    document.close()
    insert_database(lineas, "plataforma")
