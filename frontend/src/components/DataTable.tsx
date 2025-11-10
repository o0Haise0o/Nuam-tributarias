import type React from "react";

type Column<T> = {
  key: keyof T | string;
  header: string;
  render?: (row: T) => React.ReactNode;
};

export function DataTable<T extends { id: any }>({
  rows,
  columns,
}: { rows: T[]; columns: Column<T>[] }) {
  return (
    <div className="overflow-auto border rounded">
      <table className="min-w-full text-sm">
        <thead className="bg-gray-100">
          <tr>{columns.map(c => <th key={String(c.key)} className="text-left p-2">{c.header}</th>)}</tr>
        </thead>
        <tbody>
          {rows.map(r => (
            <tr key={String(r.id)} className="border-t">
              {columns.map(c => (
                <td key={String(c.key)} className="p-2">
                  {c.render ? c.render(r) : (r as any)[c.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
