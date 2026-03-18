from fastapi import FastAPI, HTTPException, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
import uvicorn
from services.consultas import obtener_tablas
from services.generar_excel import crear_excel
from services.enviar_correo import enviar_correo_smtp
from services.grafico_cartera import generar_grafico_cartera

from datetime import datetime
import pandas as pd
import os
import tempfile
import base64
from typing import Optional, Any

app = FastAPI()

# =============================
# CORS
# =============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# CACHE
# =============================

datos_cache: dict = {
    "ingresos": [],
    "cartera": [],
    "ultima_actualizacion": None
}

# =============================
# ROOT
# =============================

@app.get("/")
def root():
    return {"mensaje": "API de Reporte Cartera funcionando"}

# =============================
# STATUS
# =============================

@app.get("/status")
def status():

    return {
        "servidor": "activo",
        "ultima_actualizacion": datos_cache["ultima_actualizacion"],
        "ingresos": len(datos_cache["ingresos"]),
        "cartera": len(datos_cache["cartera"])
    }

# =============================
# ACTUALIZAR DATOS
# =============================

@app.get("/actualizar")
def actualizar():

    ingresos, cartera = obtener_tablas()

    datos_cache["ingresos"] = ingresos.to_dict("records")
    datos_cache["cartera"] = cartera.to_dict("records")

    datos_cache["ultima_actualizacion"] = datetime.now().isoformat()

    return {
        "mensaje": "Datos actualizados",
        "registros_ingresos": len(ingresos),
        "registros_cartera": len(cartera),
        "ultima_actualizacion": datos_cache["ultima_actualizacion"]
    }

# =============================
# DESCARGAR EXCEL
# =============================

@app.get("/descargar-excel")
def descargar_excel():

    try:

        if not datos_cache["ingresos"] or not datos_cache["cartera"]:

            ingresos, cartera = obtener_tablas()

        else:

            ingresos = pd.DataFrame(datos_cache["ingresos"])
            cartera = pd.DataFrame(datos_cache["cartera"])

        ruta_archivo = crear_excel(ingresos, cartera)

        if not os.path.exists(ruta_archivo):

            raise HTTPException(status_code=500, detail="Archivo no generado")

        return FileResponse(
            path=ruta_archivo,
            filename=os.path.basename(ruta_archivo),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# =============================
# GENERAR GRAFICO
# =============================

@app.get("/grafico")
def obtener_grafico():

    try:

        ingresos, cartera = obtener_tablas()

        df = cartera.rename(columns={
            "Saldo": "valor",
            "Edad": "edad",
            "Tercero": "tercero"
        })

        img = generar_grafico_cartera(df)

        return StreamingResponse(
            img,
            media_type="image/png"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Error generando gráfico: {str(e)}"
        )

# =============================
# ENVIAR CORREO
# =============================

@app.post("/enviar-correo")
async def enviar_correo(
    destinatarios: str = Form(...),
    asunto: str = Form(...),
    cuerpo: str = Form(...),
    archivo: Optional[UploadFile] = File(None)
):

    archivo_temporal = None

    # guardar archivo temporal si existe
    if archivo:

        suffix = os.path.splitext(archivo.filename)[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:

            contenido = await archivo.read()
            temp_file.write(contenido)

            archivo_temporal = temp_file.name

    # =========================
    # GENERAR GRAFICO
    # =========================

    ingresos, cartera = obtener_tablas()

    df = cartera.rename(columns={
        "Saldo": "valor",
        "Edad": "edad",
        "Tercero": "tercero"
    })

    grafico = generar_grafico_cartera(df)

    grafico_base64 = base64.b64encode(grafico.getvalue()).decode()

    cuerpo_html = f"""
    {cuerpo}
    <br><br>
    <h3>Clientes con mayor cartera vencida</h3>
    <img src="data:image/png;base64,{grafico_base64}" style="width:100%;max-width:900px;">
    """

    # =========================
    # ENVIAR CORREO
    # =========================

    resultado = enviar_correo_smtp(
        destinatarios=destinatarios,
        asunto=asunto,
        cuerpo=cuerpo_html,
        archivo_adjunto=archivo_temporal
    )

    # eliminar archivo temporal
    if archivo_temporal and os.path.exists(archivo_temporal):

        os.remove(archivo_temporal)

    if resultado:

        return {
            "success": True,
            "mensaje": "Correo enviado correctamente"
        }

    else:

        return {
            "success": False,
            "error": "Error enviando correo"
        }

# =============================
# RUN
# =============================

if __name__ == "__main__":

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="debug"
    )