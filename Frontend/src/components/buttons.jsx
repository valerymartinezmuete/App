import { useState, useEffect } from "react"

function Buttons() {

  const [fecha, setFecha] = useState(null)
  const [modal, setModal] = useState(false)
  const [loading, setLoading] = useState(false)
  const [loadingExcel, setLoadingExcel] = useState(false)
  const [mensaje, setMensaje] = useState("")
  const [archivoExcel, setArchivoExcel] = useState(null)

  const [destinatarios, setDestinatarios] = useState("@rbcol.co")
  const [asunto, setAsunto] = useState("URGENTE | Gestión inmediata cartera vencida – Clientes críticos")

  const [cuerpo, setCuerpo] = useState(`Buen día,

Estimados señores,

Adjuntamos el reporte actualizado de cartera vencida correspondiente a todas las unidades de negocio.

En el archivo se identifican clientes críticos con saldos vencidos que requieren gestión inmediata.

Solicitamos de manera prioritaria y sin excepción que los responsables de cada cliente realicen las acciones necesarias para garantizar el recaudo efectivo en el menor tiempo posible e informen a la brevedad el estado de las gestiones realizadas.

La situación actual de la cartera impacta directamente el flujo de caja de la compañía, por lo que agradecemos darle la máxima atención y urgencia.

Quedamos atentos a sus comentarios y avances.

Saludos,`)

  useEffect(() => {
    cargarEstadoInicial()
  }, [])

  const cargarEstadoInicial = async () => {

    try {

      const res = await fetch("http://127.0.0.1:8000/status")
      const data = await res.json()

      if (data.ultima_actualizacion) {
        setFecha(data.ultima_actualizacion)
      }

    } catch (error) {
      console.error("Error cargando estado:", error)
    }
  }





  const actualizarGrafico = async () => {

    setLoading(true)
    setMensaje("")

    try {

      const res = await fetch("http://127.0.0.1:8000/actualizar")
      const data = await res.json()

      if (data.error) {

        setMensaje(`Error: ${data.error}`)

      } else {

        setFecha(data.ultima_actualizacion)

        setMensaje(
          `✓ Datos actualizados. ${data.registros_cartera} registros cartera`
        )

        setTimeout(() => {
          window.location.reload()
        }, 1500)

      }

    } catch (error) {

      setMensaje(`Error de conexión: ${error.message}`)

    } finally {

      setLoading(false)

    }
  }

  useEffect(() => {

  const actualizar = () => {

    cargarGrafico()

  }

  window.addEventListener("grafico_actualizado", actualizar)

  return () => window.removeEventListener("grafico_actualizado", actualizar)

  }, [])

  const descargarExcel = async () => {

    setLoadingExcel(true)
    setMensaje("")

    try {

      const res = await fetch("http://127.0.0.1:8000/descargar-excel")

      if (!res.ok) {

        setMensaje("Error generando Excel")
        return

      }

      const blob = await res.blob()

      const url = window.URL.createObjectURL(blob)

      const a = document.createElement("a")
      a.href = url
      a.download = "reporte_cartera.xlsx"

      document.body.appendChild(a)
      a.click()
      a.remove()

      setMensaje("✓ Excel descargado")

    } catch (error) {

      setMensaje(`Error: ${error.message}`)

    } finally {

      setLoadingExcel(false)

    }
  }

  const handleArchivoExcel = (e) => {

    const archivo = e.target.files[0]

    if (archivo) {
      setArchivoExcel(archivo)
    }

  }


  const handlePaste = (e) => {

    const items = e.clipboardData.items

    for (let item of items) {

      if (item.type.indexOf("image") !== -1) {

        e.preventDefault()

        const file = item.getAsFile()

        const reader = new FileReader()

        reader.onload = function(event) {

          const img = document.createElement("img")

          img.src = event.target.result
          img.style.maxWidth = "500px"

          document.execCommand("insertHTML", false, img.outerHTML)

        }

        reader.readAsDataURL(file)

      }

    }

  }
  

  const enviarCorreo = async () => {

    if (!destinatarios.trim()) {
      alert("Ingresa destinatarios")
      return
    }

    try {

      const formData = new FormData()

      formData.append("destinatarios", destinatarios)
      formData.append("asunto", asunto)

      // convertir saltos de línea para el correo HTML
      const cuerpoHTML = cuerpo.replace(/\n/g, "<br>")
      formData.append("cuerpo", cuerpoHTML)

      if (archivoExcel) {
        formData.append("archivo", archivoExcel, archivoExcel.name)
      }

      const res = await fetch("http://127.0.0.1:8000/enviar-correo", {
        method: "POST",
        body: formData
      })

      const data = await res.json()

      if (res.ok) {

        setMensaje("✓ Correo enviado")
        setModal(false)

      } else {

        setMensaje(`Error: ${data.detail}`)

      }

    } catch (error) {

      setMensaje(`Error: ${error.message}`)

    }
  }

  return (

    <div className="mb-4">

      <button
        onClick={actualizarGrafico}
        disabled={loading}
        className="btn btn-outline-secondary me-2"
      >
        {loading ? "Actualizando..." : "Actualizar gráfico"}
      </button>

      <button
        className="btn btn-success me-2"
        onClick={descargarExcel}
        disabled={loadingExcel}
      >
        {loadingExcel ? "Generando..." : "Exportar Excel"}
      </button>

      <button
        onClick={() => setModal(true)}
        className="btn btn-primary"
      >
        Enviar correo
      </button>

      {fecha && (
        <div className="mt-2 text-muted">
          Última actualización: {new Date(fecha).toLocaleString()}
        </div>
      )}

      {mensaje && (
        <div className="alert alert-info mt-2">
          {mensaje}
        </div>
      )}

      {modal && (

        <div className="modal d-block" style={{background:"rgba(0,0,0,0.5)"}}>

          <div className="modal-dialog modal-lg">

            <div className="modal-content">

              <div className="modal-header">
                <h5>Enviar reporte</h5>
                <button
                  className="btn-close"
                  onClick={()=>setModal(false)}
                />
              </div>

              <div className="modal-body">

                <input
                  className="form-control mb-2"
                  value={destinatarios}
                  onChange={(e)=>setDestinatarios(e.target.value)}
                  placeholder="Destinatarios"
                />

                <input
                  className="form-control mb-2"
                  value={asunto}
                  onChange={(e)=>setAsunto(e.target.value)}
                />

                <div
                  className="form-control mb-2"
                  contentEditable
                  style={{minHeight:"200px", overflow:"auto"}}
                  dangerouslySetInnerHTML={{__html: cuerpo.replace(/\n/g, "<br>")}}
                  onInput={(e)=>setCuerpo(e.currentTarget.innerHTML)}
                  onPaste={handlePaste}
                />

                <input
                  type="file"
                  className="form-control"
                  accept=".xlsx"
                  onChange={handleArchivoExcel}
                />

              </div>

              <div className="modal-footer">

                <button
                  className="btn btn-secondary"
                  onClick={()=>setModal(false)}
                >
                  Cancelar
                </button>

                <button
                  className="btn btn-primary"
                  onClick={enviarCorreo}
                >
                  Enviar
                </button>

              </div>

            </div>

          </div>

        </div>

      )}

    </div>

  )
}

export default Buttons