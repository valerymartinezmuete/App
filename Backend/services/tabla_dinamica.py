import pandas as pd

def crear_tabla_dinamica(ingresos, cartera, areas_filtrar=None):

    datos = ingresos.copy()

    # Traer la Unidad de Negocio desde cartera
    mapa_areas = cartera[["Tercero","Unidad de Negocio"]].drop_duplicates()

    datos = datos.merge(mapa_areas, on="Tercero", how="left")

    # Convertir fecha
    datos["Fecha"] = pd.to_datetime(datos["Fecha"])

    datos["Año"] = datos["Fecha"].dt.year
    datos["Trimestre"] = "Trim." + datos["Fecha"].dt.quarter.astype(str)
    datos["Mes"] = datos["Fecha"].dt.strftime("%b")

    # Filtrar áreas
    if areas_filtrar:
        datos = datos[datos["Unidad de Negocio"].isin(areas_filtrar)]

    pivot = pd.pivot_table(
        datos,
        index=["Unidad de Negocio","Tercero"],
        columns=["Año","Trimestre","Mes"],
        values="Saldo",
        aggfunc="sum",
        fill_value=0
    )

    pivot["Total general"] = pivot.sum(axis=1)

    return pivot.reset_index()