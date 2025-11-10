import axios from "axios";
import { api, type Paginated } from "./client";

export type Calificacion = {
  id: string;
  mercado: "CL" | "US" | "EU";
  origen_texto: string;
  periodo_comercial: string; // YYYY-MM-DD
  instrumento: string;
  fecha_pago?: string | null;
  descripcion: string;
  secuencia_evento: string;
  monto: string;
  dividendo: string;
  habilitado: boolean;
  factor: string;
  origen?: number | null;
};

export async function listCalificaciones(params: Record<string, any>) {
  const { data } = await api.get<Paginated<Calificacion>>("/calificaciones/", { params });
  return data;
}
export const createCalificacion = async (data: any) => {
  try {
    const response = await api.post("/calificaciones/", data); 
    console.log("Demo creado exitosamente:", response.data);
    return response.data;
  } catch (error) {
    console.error("Error al crear calificación:", error);
    throw error;
  }
};


export async function updateCalificacion(id: string, payload: Partial<Calificacion>) {
  const { data } = await api.patch<Calificacion>(`/calificaciones/${id}/`, payload);
  return data;
}
export async function deleteCalificacion(id: string) {
  await api.delete(`/calificaciones/${id}/`);
}

export async function exportCSV(params: Record<string, any>) {
  const res = await api.get("/calificaciones/export/", { params, responseType: "blob" });
  return res.data; 
}

export async function previewCSV(file: File) {
  const form = new FormData();
  form.append("file", file);
  const { data } = await api.post("/calificaciones/preview-csv/", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data as { total_filas: number; muestras: any[]; errores: any[]; ok: boolean };
}
export async function bulkUpload(file: File, meta?: Record<string, any>) {
  const form = new FormData();
  form.append("file", file);
  if (meta) Object.entries(meta).forEach(([k, v]) => form.append(k, String(v)));
  const { data } = await api.post("/calificaciones/bulk-upload/", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data as { origen_id: number; creados: number };
}
export async function cancelarImportacion(origen_id: number) {
  const { data } = await api.post("/calificaciones/cancelar-importacion/", { origen_id });
  return data as { eliminadas: number; origen_id: number };
}
