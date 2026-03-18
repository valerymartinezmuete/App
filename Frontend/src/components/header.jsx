export default function Header() {
  return (
    <div className="Header d-flex justify-content-between align-items-center mb-4">

      <div className="d-flex align-items-center gap-3">
        <div className="icono-reporte">📊</div>

        <div>
          <h4 className="mb-0">
            Reporte de Cartera · Russell Bedford
          </h4>
          <small className="text-muted">
            Sistema de análisis financiero
          </small>
        </div>
      </div>

    </div>
  );
}