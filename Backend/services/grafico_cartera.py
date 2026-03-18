import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from io import BytesIO


def generar_grafico_cartera(df):

    df["edad"] = pd.to_numeric(df["edad"], errors="coerce").fillna(0)
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0)

    # clasificar por edades
    df["0_30"] = np.where(df["edad"] <= 30, df["valor"], 0)
    df["31_60"] = np.where((df["edad"] > 30) & (df["edad"] <= 60), df["valor"], 0)
    df["61_90"] = np.where((df["edad"] > 60) & (df["edad"] <= 90), df["valor"], 0)
    df["90_mas"] = np.where(df["edad"] > 90, df["valor"], 0)

    resumen = df.groupby("tercero")[["0_30","31_60","61_90","90_mas"]].sum()

    resumen["total"] = resumen.sum(axis=1)

    resumen = resumen.sort_values("total", ascending=False).head(20)

    y = np.arange(len(resumen))

    fig, ax = plt.subplots(figsize=(14,8))

    azul = "#2C7BE5"
    morado = "#6A4C93"
    naranja = "#F4A261"
    rojo = "#E63946"

    ax.barh(y, resumen["0_30"], color=azul, label="0-30 días")

    ax.barh(
        y,
        resumen["31_60"],
        left=resumen["0_30"],
        color=morado,
        label="31-60 días"
    )

    ax.barh(
        y,
        resumen["61_90"],
        left=resumen["0_30"] + resumen["31_60"],
        color=naranja,
        label="61-90 días"
    )

    ax.barh(
        y,
        resumen["90_mas"],
        left=resumen["0_30"] + resumen["31_60"] + resumen["61_90"],
        color=rojo,
        label="90+ días"
    )

    ax.set_yticks(y)
    ax.set_yticklabels(resumen.index)

    ax.invert_yaxis()

    ax.set_title("Clientes con mayor cartera vencida")

    # etiquetas con valor total
    for i, total in enumerate(resumen["total"]):

        texto = f"${total/1000000:.1f}M"

        ax.text(
            total,
            i,
            texto,
            va="center",
            ha="left",
            fontsize=9
        )

    # ax.legend()

    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=300)
    plt.close()

    buffer.seek(0)

    return buffer