import { useEffect, useState } from "react";

function Reporte() {

  const [datos, setDatos] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/reporte")
      .then(res => res.json())
      .then(data => setDatos(data.data));
  }, []);

  return (
    <div>
      <h1>Reporte</h1>

      {datos.map((fila, index) => (
        <div key={index}>{JSON.stringify(fila)}</div>
      ))}
    </div>
  );
}

export default Reporte;