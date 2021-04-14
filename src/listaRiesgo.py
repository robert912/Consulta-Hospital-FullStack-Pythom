import mysql.connector
from mysql.connector import Error

#Funcio que retorna una lista de pacientes que pertenecen a la consulta pediatria
def listaPediatria():
    cursor.execute("Select *, (edad*historia_clinica)/100 as Riesgo from paciente where id_consulta = 1 order by historia_clinica desc")
    return cursor.fetchall()

#Funcio que retorna una lista de pacientes que pertenecen a la consulta de Urgencia
def listaUrgencia():
    cursor.execute("Select *, (edad*historia_clinica)/100 as Riesgo from paciente where id_consulta = 2 order by historia_clinica desc")
    resultados = cursor.fetchall()
    lista = []
    for fila in resultados:
        lista.append(list(fila))
    for fila in lista:
        if (fila[2] > 40):
            fila[5] += 5.3
    return lista

#Funcio que retorna una lista de pacientes que pertenecen a la consulta General Integral
def listaCGI():
    cursor.execute("Select *, (edad*historia_clinica)/100 as Riesgo from paciente where id_consulta = 3 order by historia_clinica desc")
    resultados = cursor.fetchall()
    lista = []
    for fila in resultados:
        lista.append(list(fila))
    for fila in lista:
        if (fila[2] > 40):
            fila[5] += 5.3
    return lista


try:
    conexion = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='12345678',
        db='hospital'
    )
    if conexion.is_connected():
        print("Conexion Exitosa.")
        cursor=conexion.cursor()
        pediatria = listaPediatria()
        urgencia = listaUrgencia()
        cgi = listaCGI()
    
except Error as ex:
    print("Error durante la Conexion", ex)

finally:
    if conexion.is_connected():
        conexion.close() # Se cerro la conexion a la BD
        print("La Conexion ha finalizado")

