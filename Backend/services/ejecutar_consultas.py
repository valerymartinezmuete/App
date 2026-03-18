from pathlib import Path

import pandas as pd


def ejecutar_consultas():
    """Ejecuta el SQL definido en consultas/consultas.sql usando la conexión configurada."""
    # import dinámico para evitar errores de análisis estático
    conexion_cadena_bd = __import__("database.conexion", fromlist=["conexion_cadena_bd"]).conexion_cadena_bd

    conn = conexion_cadena_bd()

    sql_path = Path(__file__).resolve().parent.parent / "consultas" / "consultas.sql"
    with sql_path.open("r", encoding="utf-8") as f:
        query = f.read()

    df = pd.read_sql(query, conn)
    conn.close()
    return df
