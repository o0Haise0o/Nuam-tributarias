import { Link } from "react-router-dom";

export default function Home() {
  return (
    <section className="space-y-8">
      <div className="rounded-3xl bg-gradient-to-r from-nuam-50 to-white border border-nuam-100 p-8">
        <h1 className="text-3xl md:text-4xl font-bold text-slate-900">
          NUAM – Mantenedor de Calificaciones Tributarias
        </h1>
        <p className="mt-2 text-slate-600 max-w-2xl">
          Consulta, carga y gestiona calificaciones con trazabilidad completa.
        </p>

        <div className="mt-6 flex flex-wrap gap-3">
          <Link to="/calificaciones" className="btn-primary">Ir a Calificaciones</Link>
          <Link to="/bulk" className="btn-outline">Carga Masiva (CSV)</Link>
          <Link to="/audit" className="btn-ghost">Ver Auditoría</Link>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <div className="card"><div className="card-body">
          <h3 className="card-title">Consulta / Gestión</h3>
          <p className="text-slate-600 text-sm">Filtra por período, instrumento, mercado y edita registros.</p>
        </div></div>

        <div className="card"><div className="card-body">
          <h3 className="card-title">Carga Masiva</h3>
          <p className="text-slate-600 text-sm">Importa CSV validados con opción de cancelar la importación.</p>
        </div></div>

        <div className="card"><div className="card-body">
          <h3 className="card-title">Auditoría</h3>
          <p className="text-slate-600 text-sm">Historial de altas, bajas, modificaciones y cargas masivas.</p>
        </div></div>
      </div>
    </section>
  );
}
