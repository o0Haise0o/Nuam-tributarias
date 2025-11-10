import { useEffect, useState } from "react";
import {  listAudit, type Audit } from "../api/audit";
import { DataTable } from "../components/DataTable";

export default function AuditList() {
  const [rows, setRows] = useState<Audit[]>([]);
  useEffect(() => {
    (async () => {
      const data = await listAudit({ page_size: 100 });
      setRows(data.results);
    })();
  }, []);
  return (
    <div className="p-6 space-y-4">
      <h2 className="text-xl font-semibold">Auditoría</h2>
      <DataTable
        rows={rows}
        columns={[
          { key: "timestamp", header: "Fecha" },
          { key: "action", header: "Acción" },
          { key: "entity", header: "Entidad" },
          { key: "entity_id", header: "ID" },
          { key: "user", header: "Usuario" },
        ]}
      />
    </div>
  );
}
