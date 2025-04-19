import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Temporaria1@",  # ⚠️ Ideal mover isso para variável de ambiente futuramente
        database="db_controle_estoque_fecaf"
    )
