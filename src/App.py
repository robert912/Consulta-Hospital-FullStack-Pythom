from flask import Flask, render_template, jsonify, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
from listaRiesgo import pediatria, urgencia, cgi

#Clase Paciente
class Paciente:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
        self.noHistoriaClinica = 0

#clase Niño que hereda de Paciente, permite obtener la prioridad del paciente
class PNinno(Paciente):
    def prioridadNinio(self, edad, pesoEstatura):
        self.edad = edad
        self.pesoEstatura = pesoEstatura
        if(self.edad >= 0 and self.edad <=5):
            return self.pesoEstatura + 3
        elif(self.edad >= 6 and self.edad <=12):
            return self.pesoEstatura + 2
        else:
            return self.pesoEstatura + 1

#clase joven que hereda de Paciente, permite obtener la prioridad del paciente
class PJoven(Paciente):
    def prioridadJoven(self, anioFumador):
        self.anioFumador = anioFumador
        if(anioFumador == 0):
            return 2
        else:
            return (anioFumador/4) + 2

#clase Anciano que hereda de Paciente, permite obtener la prioridad del paciente
class PAnciano(Paciente):
    def prioridadAnciano(self, edad, dieta):
        self.dieta = dieta
        self.edad = edad
        if(self.dieta and self.edad >= 60 and self.edad <=100):
            return (self.edad/20) + 4
        else:
            return (self.edad/30) + 3

app = Flask(__name__)

#Conexion a la Base de Datos
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
    
    paciente = Paciente("",0)

#Pagina principal en donde se encuentra Optimzada la atencion por gravedad de cada paciente y segun su tipo de consulta
    @app.route('/')
    def index():
        cursor=conexion.cursor()
        cursor.execute("Select * from consulta")
        consultas = cursor.fetchall()
        return render_template("index.html", consulta = consultas, pediatria = pediatria, urgencia = urgencia, cgi = cgi)


#Funcion principal para agregar un paciente
    @app.route('/add_paciente')
    def add_paciente():
        return render_template("add_paciente.html")

#Funcion Atender Paciente
    @app.route('/atender/<string:id>')
    def atender_paciente(id):
        cursor=conexion.cursor()
        cursor.execute("SELECT num_pacientes_atendido, estado from consulta where id_consulta = {0};".format(id))
        consulta = cursor.fetchone()
        if(consulta[1]):
            estado = 0
        else:
            estado = 1
        cursor.execute("update consulta set num_pacientes_atendido = '{0}', estado = {1} where id_consulta = {2};".format(consulta[0]+1, estado, id))
        conexion.commit()# Confirmar la accion que estamos ejecutando.
        print("Registro Actualizado con exito")
        return redirect(url_for('index'))

#Funcion Liberar Consulta
    @app.route('/liberar/<string:id>')
    def liberar_consulta(id):
        cursor=conexion.cursor()
        cursor.execute("SELECT estado from consulta where id_consulta = {0};".format(id))
        consulta = cursor.fetchone()
        if(consulta[0]):
            estado = 0
        else:
            estado = 1
        cursor.execute("update consulta set estado = {0} where id_consulta = {1};".format(estado, id))
        conexion.commit()# Confirmar la accion que estamos ejecutando.
        print("Registro Actualizado con exito")
        tipoConsulta = int(id)
        if(tipoConsulta == 1):
            pediatria.pop(0)
            for fila in pediatria:
                print(fila[0], fila[1], fila[2])
        elif(tipoConsulta == 2):
            urgencia.pop(0)
        else:
            cgi.pop(0)
        return redirect(url_for('index'))

#funcion que permite agregar un tipo de atributo a cada tipo de paciente
    @app.route('/tipo_paciente', methods=["POST"])
    def tipo_paciente():
        if request.method == 'POST':
            paciente.nombre = request.form.get("inputNombre")
            paciente.edad = int(request.form.get("inputEdad"))
            if (paciente.edad >= 0 and paciente.edad <= 15):
                return render_template("add_ninio.html", nombre = paciente.nombre, edad = paciente.edad)
            elif(paciente.edad >= 16 and paciente.edad <= 40):
                return render_template("add_joven.html", nombre = paciente.nombre, edad = paciente.edad)
            else:
                return render_template("add_anciano.html", nombre = paciente.nombre, edad = paciente.edad)

#Funcionalidad que inserta a un nuevo Paciente a la Base de datos, el Historia clinico y el tipo de consulta se saca en base a un calculo segun el tipo de Paciente y su edad
    @app.route('/insertar', methods=["POST"])
    def insertar():
        if request.method == 'POST':
            consulta = 0
            if (paciente.edad >= 0 and paciente.edad <= 15):
                pesoEstatura = int(request.form.get("inputPesoEstatura"))
                ninio = PNinno(paciente.nombre, paciente.edad)
                paciente.noHistoriaClinica = ninio.prioridadNinio(ninio.edad, pesoEstatura)
                if(paciente.noHistoriaClinica > 4):
                    consulta = 2
                else:
                    consulta = 1
            elif(paciente.edad >= 16 and paciente.edad <= 40):
                fumador = int(request.form.get("inputfumador"))
                joven = PJoven(paciente.nombre, paciente.edad)
                paciente.noHistoriaClinica = joven.prioridadJoven(fumador)
                if(paciente.noHistoriaClinica > 4):
                    consulta = 2
                else:
                    consulta = 3
            else:
                dieta = int(request.form.get("inputDieta"))
                anciano = PAnciano(paciente.nombre, paciente.edad)
                paciente.noHistoriaClinica = anciano.prioridadAnciano(anciano.edad, dieta)
                if(paciente.noHistoriaClinica > 4):
                    consulta = 2
                else:
                    consulta = 3

            cursor=conexion.cursor()
            sentencia = "Insert into paciente (nombre, edad, historia_clinica, id_consulta) values('{0}', {1}, {2}, {3});".format(paciente.nombre, paciente.edad, paciente.noHistoriaClinica, consulta)
            cursor.execute(sentencia)
            conexion.commit()# Confirmar la accion que estamos ejecutando.
            print("Registro Insertado con exito")
            return redirect(url_for('index'))

#Funcionlidad que Lista los pacientes con mayor riesgo ordenados desde el mayor a menor prioridad segun su historial clinico
    @app.route('/listar')
    def listar_Pacientes_Mayor_Riesgo():
        cursor=conexion.cursor()
        cursor.execute("Select *, (edad*historia_clinica)/100 as Riesgo from paciente order by Riesgo desc;")
        resultados = cursor.fetchall()
        lista = []
        for fila in resultados:
            lista.append(list(fila))
        for fila in lista:
            if (fila[2] > 40):
                fila[5] += 5.3
        return render_template("listar.html",lista = lista)

#Funcionlidad que Lista los pacientes fumadores y que pertenecen a la consulta de urgencia
    @app.route('/listarFumadores')
    def listar_Pacientes_fumadores_urgentes():
        cursor=conexion.cursor()
        cursor.execute("Select * from paciente where id_consulta = 2 and edad >=16 and edad <=40 order by historia_clinica desc;")
        resultados = cursor.fetchall()
        return render_template("fumador.html",lista = resultados)

#funcionalidad que devuelve la consulta con mas pacientes atendidos
    @app.route('/pacientes_por_consulta')
    def consulta_mas_pacientes_atendidos():
        cursor=conexion.cursor()
        cursor.execute("select * from consulta where num_pacientes_atendido = (Select max(num_pacientes_atendido) from consulta);")
        consultaMayor = cursor.fetchone()
        return render_template("top_consulta.html",consult = consultaMayor)

#funcionalidad que devuelve el paciente mas Anciano
    @app.route('/mayor')
    def paciente_mas_anciano():
        cursor=conexion.cursor()
        cursor.execute("select * from paciente where edad = (Select max(edad) from paciente);")
        anciano = cursor.fetchone()
        return render_template("personaMayor.html",anciano = anciano)


    if __name__ == '__main__':
        app.run(host="127.0.0.1", port=5000, debug=True)# (debug=True)permite reiniciar el servido cada vez que se haga un cambio


except Error as ex:
    print("Error durante la Conexion", ex)

finally:
    if conexion.is_connected():
        conexion.close() # Se cerro la conexion a la BD
        print("La Conexion ha finalizado")


