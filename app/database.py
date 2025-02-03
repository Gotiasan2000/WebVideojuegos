import mysql.connector

# Configuración de la conexión
def get_db_connection():
    return mysql.connector.connect(
        host="informatica.iesquevedo.es",
        port=3333,
        user="root",
        password="1asir",
        database="Santiago"  
    )