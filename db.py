#CONECCION A BD
import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",      # Tu contraseña de MySQL si la configuraste
        database="pañalera"
    )