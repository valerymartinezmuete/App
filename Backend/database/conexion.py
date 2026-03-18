import psycopg

dbname = "KristallDevelopment"
user = "K_1_Consulta_ADM"
host = "kristal-database.cwhuotuvqupr.us-east-1.rds.amazonaws.com"
port = "5432"
password = "W+DiI6p6f,ZEH}HBRMm!]7"

def conexion_cadena_bd():
    try:
        conexion = psycopg.connect(
            f"""
            dbname={dbname}
            user={user}
            host={host}
            port={port}
            password={password}
            """,
            connect_timeout=90,
            prepare_threshold=3,
            keepalives=1,
            keepalives_idle=15,
            keepalives_interval=5,
            keepalives_count=10
        )
        return conexion
    except psycopg.Error as e:
        print(f"Error en la conexión a la base de datos: {e}")
        raise