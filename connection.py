import psycopg2

try:
    conn = psycopg2.connect(
        dbname="Fitrack_db",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    print("Conexión exitosa a PostgreSQL.")
except Exception as e:
    print(f"Error de conexión: {e}")
