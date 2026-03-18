import pandas as pd


def crear_tabla_facturacion(ingresos):

    # asegurar fecha correcta
    ingresos["Fecha"] = pd.to_datetime(ingresos["Fecha"])

    # eliminar hora
    ingresos["Fecha"] = ingresos["Fecha"].dt.date

    # crear columna mes
    ingresos["Mes"] = pd.to_datetime(ingresos["Fecha"]).dt.strftime("%b %Y")

    # pivot tabla
    tabla = ingresos.pivot_table(
        index=["Empresa", "Tercero"],
        columns="Mes",
        values="Saldo",
        aggfunc="sum",
        fill_value=0
    )

    # ordenar meses
    tabla = tabla.sort_index(axis=1, ascending=False)

    # tendencia ingreso
    tabla["Tendencia Ingreso"] = tabla.sum(axis=1)

    # ordenar columnas
    cols = ["Tendencia Ingreso"] + [c for c in tabla.columns if c != "Tendencia Ingreso"]

    tabla = tabla[cols]

    # reset index
    tabla = tabla.reset_index()

    # renombrar columnas
    tabla = tabla.rename(columns={
        "Empresa": "Empresa",
        "Tercero": "Cliente"
    })

    return tabla