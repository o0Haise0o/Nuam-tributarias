import { useEffect, useState } from "react";
import { type Calificacion, listCalificaciones, exportCSV, createCalificacion, updateCalificacion, deleteCalificacion } from "../api/calificaciones";

type EditPayload = {
  periodo_comercial: string;
  monto: string;
  dividendo: string;
  habilitado: boolean;
  factor: string;
  descripcion: string;
}

export default function CalificacionesList() {
  const [rows, setRows] = useState<Calificacion[]>([]);
  const [editingCalificacion, setEditingCalificacion] = useState<Calificacion | null>(null);

  const [q] = useState({ search: "", mercado: "", periodo_comercial__gte: "", periodo_comercial__lte: "" });

  async function load() {
    const data = await listCalificaciones({
      search: q.search || undefined,
      mercado: q.mercado || undefined,
      periodo_comercial__gte: q.periodo_comercial__gte || undefined,
      periodo_comercial__lte: q.periodo_comercial__lte || undefined,
      ordering: "-periodo_comercial",
      page_size: 100,
    });
    setRows(data.results);
  }

  useEffect(() => { load(); }, []); 

  async function onExport() {
    const blob = await exportCSV({
      search: q.search || undefined,
      mercado: q.mercado || undefined,
      periodo_comercial__gte: q.periodo_comercial__gte || undefined,
      periodo_comercial__lte: q.periodo_comercial__lte || undefined,
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = "calificaciones.csv"; a.click();
    URL.revokeObjectURL(url);
  }

  async function quickCreate() {
    const randomSuffix = Math.floor(Math.random() * 1000); 
    
    await createCalificacion({
      mercado: "CL",
      periodo_comercial: "2025-01-01",
      instrumento: `BCH-${randomSuffix}`, 
      monto: "1000.00",
      dividendo: "0",
      habilitado: true,
      factor: "1",
      origen_texto: "manual",
      descripcion: "",
      secuencia_evento: "",
    });
    await load(); 
  }


  function onEdit(calif: Calificacion) {
    setEditingCalificacion(calif);
  }

  function onCancelEdit() {
    setEditingCalificacion(null);
  }

  async function onDelete(id: string, instrumento: string) {
    if (!window.confirm(`¿Estás seguro de que quieres eliminar la calificación ${instrumento}? Esta acción es irreversible.`)) {
      return;
    }
    try {
      await deleteCalificacion(id);
      alert(`Calificación ${instrumento} eliminada correctamente.`);
      await load();
    } catch (error) {
      console.error("Error al eliminar:", error);
      alert("Error al intentar eliminar la calificación. Revisa la consola.");
    }
  }

  function handleFormChange(e: React.ChangeEvent<HTMLInputElement>) {
    const { name, value, type, checked } = e.target;
    setEditingCalificacion((prev) => {
      if (!prev) return null;
      return {
        ...prev,
        [name]: type === 'checkbox' ? checked : value
      } as Calificacion; 
    });
  }

  async function onSaveEdit(e: React.FormEvent) {
    e.preventDefault();
    if (!editingCalificacion) return;
    
    try {
      const payload: EditPayload = {
          periodo_comercial: editingCalificacion.periodo_comercial,
          monto: editingCalificacion.monto, 
          dividendo: editingCalificacion.dividendo,
          habilitado: editingCalificacion.habilitado,
          factor: editingCalificacion.factor,
          descripcion: editingCalificacion.descripcion,
      };
      
      await updateCalificacion(editingCalificacion.id, payload);
      alert("Calificación actualizada con éxito.");
      onCancelEdit(); 
      await load(); 
    } catch (error) {
      console.error("Error al actualizar calificación:", error);
      alert("Error al actualizar: Asegúrate de que los datos sean válidos.");
    }
  }

  return (
    <section className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Calificaciones</h2>
        <div className="flex gap-2">
          <button onClick={onExport} className="btn-outline">Exportar CSV</button>
          <button onClick={quickCreate} className="btn-primary">Crear demo</button>
        </div>
      </div>

      <div className="card">
        <div className="card-body">
          <table className="table">
            <thead>
              <tr>
                <th className="th">Instrumento</th>
                <th className="th">Periodo</th>
                <th className="th">Monto</th>
                <th className="th">Estado</th>
                <th className="th">Acciones</th> 
              </tr>
            </thead>
            <tbody>
             {rows.map((calif) => (
                <tr key={calif.id}>
                  <td>{calif.instrumento}</td>
                  <td>{calif.periodo_comercial}</td>
                  <td>{calif.monto}</td>
                  <td>{calif.habilitado ? "Habilitado" : "Deshabilitado"}</td>
                  <td>
                    <div className="flex gap-2">
                      <button 
                        onClick={() => onEdit(calif)} 
                        className="text-blue-600 hover:text-blue-800 text-sm"
                      >
                        Editar
                      </button>
                      <button 
                        onClick={() => onDelete(calif.id, calif.instrumento)} 
                        className="text-red-600 hover:text-red-800 text-sm"
                      >
                        Eliminar
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      
      {editingCalificacion && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-lg">
            <h3 className="text-lg font-bold mb-4">
              Editar Calificación: {editingCalificacion.instrumento}
            </h3>
            
            <form onSubmit={onSaveEdit} className="space-y-4">
              
              <div>
                <label className="block text-sm font-medium text-gray-700">Periodo Comercial</label>
                <input
                  
                  type="date" 
                  name="periodo_comercial"
                  value={editingCalificacion.periodo_comercial}
                  onChange={handleFormChange}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">Monto</label>
                <input
                  type="number"
                  name="monto"
                  value={editingCalificacion.monto}
                  onChange={handleFormChange}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2"
                  step="0.01"
                />
              </div>

              
              <div>
                <label className="block text-sm font-medium text-gray-700">Factor</label>
                <input
                  type="number"
                  name="factor"
                  value={editingCalificacion.factor}
                  onChange={handleFormChange}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2"
                  step="0.000001"
                />
              </div>

              
              <div>
                <label className="block text-sm font-medium text-gray-700">Descripción</label>
                <input
                  type="text"
                  name="descripcion"
                  value={editingCalificacion.descripcion}
                  onChange={handleFormChange}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2"
                />
              </div>

              
              <div className="flex items-center">
                <input
                  id="habilitado"
                  name="habilitado"
                  type="checkbox"
                  checked={editingCalificacion.habilitado}
                  onChange={handleFormChange}
                  className="h-4 w-4 text-indigo-600 border-gray-300 rounded"
                />
                <label htmlFor="habilitado" className="ml-2 block text-sm text-gray-900">
                  Habilitado
                </label>
              </div>
              
              <div className="flex justify-end space-x-3 pt-4">
                <button 
                  type="button" 
                  onClick={onCancelEdit} 
                  className="bg-gray-200 text-gray-700 font-semibold py-2 px-4 rounded hover:bg-gray-300"
                >
                  Cancelar
                </button>
                <button 
                  type="submit" 
                  className="btn-primary" 
                >
                  Guardar Cambios
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </section>
  );
}