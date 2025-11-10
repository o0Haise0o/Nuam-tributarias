import { api, type Paginated } from "./client";
export type Audit = { id: number; entity: string; entity_id: string; action: string; user: string; before: any; after: any; origen: number|null; timestamp: string; };
export async function listAudit(params: Record<string, any>) {
  const { data } = await api.get<Paginated<Audit>>("/audit/", { params });
  return data;
}
