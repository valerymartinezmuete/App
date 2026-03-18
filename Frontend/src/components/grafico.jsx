import { useEffect, useState } from "react"

function Grafico() {

  const [grafico, setGrafico] = useState(null)

  const cargarGrafico = async () => {

    try {

      const res = await fetch("http://127.0.0.1:8000/grafico")

      if (!res.ok) {
        throw new Error("Error cargando gráfico")
      }

      const blob = await res.blob()

      const url = URL.createObjectURL(blob)

      setGrafico(url)

    } catch (error) {

      console.error(error)

    }

  }

  useEffect(() => {

    cargarGrafico()

  }, [])

  useEffect(() => {

  const actualizar = () => {

    cargarGrafico()

  }

  window.addEventListener("grafico_actualizado", actualizar)

  return () => {

    window.removeEventListener("grafico_actualizado", actualizar)

  }

}, [])

  return (

    <div className="mt-4">

      <h4>Clientes con mayor cartera vencida</h4>

      {grafico ? (

        <img
          src={grafico}
          style={{
            width: "100%",
            maxWidth: "1200px",
            borderRadius: "6px"
          }}
        />

      ) : (

        <p>Cargando gráfico...</p>

      )}

    </div>

  )

}

export default Grafico