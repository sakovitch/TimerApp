import mysql.connector

def get_database_connection():
    return mysql.connector.connect(
        host="localhost",           # Host je "localhost", pretože ide o lokálny server
        user="root",                # Používateľské meno je "root"
        password="warcraft3",                # Heslo je prázdne (ak ste nenastavili heslo pri inštalácii MySQL)
        database="moja_databaza",   # Názov databázy, ktorú ste vytvorili
        port=3306                   # Štandardný port pre MySQL
    )
