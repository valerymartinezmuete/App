import base64
import os
import requests
import msal

# ==============================
# CONFIGURACION MICROSOFT GRAPH
# ==============================

CLIENT_ID = "caf057b1-5a09-4edc-b99e-e895fb9e7fd7"
TENANT_ID = "89fdd17b-658f-4c11-aa8f-1094e5d93d91"
import os
client_secret = os.getenv("CLIENT_SECRET")

AUTHORITY_URL = f"https://login.microsoftonline.com/{TENANT_ID}"

REMITENTE = "automation@rbcol.co"

GRAPH_ENDPOINT = f"https://graph.microsoft.com/v1.0/users/{REMITENTE}/sendMail"


# ==============================
# OBTENER TOKEN
# ==============================

def obtener_token():

    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY_URL,
        client_credential=client_secret
    )

    scopes = ["https://graph.microsoft.com/.default"]

    result = app.acquire_token_for_client(scopes=scopes)

    if "access_token" in result:
        print("Token obtenido correctamente")
        return result["access_token"]

    print("Error obteniendo token:", result)
    return None


# ==============================
# ENVIAR CORREO
# ==============================

def enviar_correo_smtp(destinatarios, asunto, cuerpo, archivo_adjunto=None):

    token = obtener_token()

    if not token:
        print("No se pudo obtener token")
        return False

    # convertir destinatarios a formato Graph
    lista_destinatarios = [
        {"emailAddress": {"address": email.strip()}}
        for email in destinatarios.split(",")
    ]

    attachments = []

    if archivo_adjunto and os.path.exists(archivo_adjunto):

        with open(archivo_adjunto, "rb") as f:
            contenido = f.read()

        excel_b64 = base64.b64encode(contenido).decode("utf-8")

        attachments.append({
            "@odata.type": "#microsoft.graph.fileAttachment",
            "name": "reporte de cartera.xlsx",
            "contentType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "contentBytes": excel_b64
        })

    email_message = {
        "message": {
            "subject": asunto,
            "body": {
                "contentType": "HTML",
                "content": cuerpo
            },
            "toRecipients": lista_destinatarios,
            "attachments": attachments
        },
        "saveToSentItems": True
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        GRAPH_ENDPOINT,
        headers=headers,
        json=email_message
    )

    if response.status_code == 202:
        print("Correo enviado correctamente")
        return True

    print("Error enviando correo:", response.text)
    return False