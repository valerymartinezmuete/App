"""Module for database queries related to portfolio and income reports."""
import pandas as pd


def obtener_tablas(areas_filtrar=None):
    """Obtiene las tablas de ingresos y cartera con filtro opcional de áreas"""
    
    # import dinámico para evitar errores de análisis estático
    conexion_cadena_bd = __import__("database.conexion", fromlist=["conexion_cadena_bd"]).conexion_cadena_bd
    conn = conexion_cadena_bd()

    # consulta ingresos - filtros más permisivos
    query_ingresos = """
    select
        "Fecha",
        "Empresa",
        "Saldo",
        "Tercero"
    from public."Movimientos"
    where
        "Fecha" >= '2026-01-01'
        and "Empresa" in ('RBG CONSULTING SAS BIC', 'RBG LEGAL SAS BIC', 'Russell Bedford', 'ARA')
        and "Cod_Clase" = '4'
        and "Fecha" is not null
        and "Empresa" is not null
        and "Saldo" is not null"""

    # Agregar filtro de áreas si se especifica (filtrar por empresa ya que Movimientos puede no tener Unidad de Negocio)
    if areas_filtrar:
        # Para ingresos, filtramos por empresa relacionada con las áreas
        empresas_por_area = {
            'Consultoria': ['RBG CONSULTING SAS BIC'],
            'Legal': ['RBG LEGAL SAS BIC'],
            'Auditoria': ['RUSSELL BEDFORD RBG S.A.S. BIC', 'Russell Bedford'],
            'Otro': ['ARA CONSULTING SAS', 'ARA']
        }
        empresas_filtrar = []
        for area in areas_filtrar:
            if area in empresas_por_area:
                empresas_filtrar.extend(empresas_por_area[area])
        if empresas_filtrar:
            empresas_str = ",".join(f"'{emp}'" for emp in empresas_filtrar)
            query_ingresos += f" and \"Empresa\" IN ({empresas_str})"

    query_ingresos += ";"

    # consulta cartera - filtros más permisivos
    query_cartera = """
        select
        "Empresa",
        "Unidad de Negocio",
        "Tercero",
        "Tipo Documento",
        "Número Documento",
        "Fecha Vencimiento",
        "Edad",
        "Mora",
        "Saldo",
        nombre_vendedor
    from public."Cartera Abierta"
    where
        "Empresa" in ('RBG CONSULTING SAS BIC', 'RBG LEGAL SAS BIC', 'RUSSELL BEDFORD RBG S.A.S. BIC', 'ARA CONSULTING SAS')
        and "Edad" in ('Ven. 181 a 360', 'Ven. 361 a 720', 'Ven. 61 a 90', 'Ven. 721 a 9999', 'Ven. 91 a 180')
        and "Empresa" is not null
        and "Saldo" is not null
        and "Tipo Documento" = 'FEV'"""

    # Agregar filtro de áreas si se especifica
    if areas_filtrar:
        areas_str = ",".join(f"'{area}'" for area in areas_filtrar)
        query_cartera += f" and \"Unidad de Negocio\" IN ({areas_str})"

    query_cartera += ";"

    ingresos = pd.read_sql(query_ingresos, conn)
    cartera = pd.read_sql(query_cartera, conn)

    conn.close()

    return ingresos, cartera