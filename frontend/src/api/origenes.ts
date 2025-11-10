import { api, Paginated } from "./client";
export type Origen = { id: number; fecha: string; archivo: string; tipo_ingreso: string; encargado: string; observaciones: string; validado_formato: boolean; };
export async function listOrigenes(params: Record<string, any>) {
  const { data } = await api.get<Paginated<Origen>>("/origenes/", { params });
  return data;
}
