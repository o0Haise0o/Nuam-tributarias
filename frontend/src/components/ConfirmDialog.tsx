export function ConfirmDialog({ text, onConfirm }: { text: string; onConfirm: () => void }) {
  return (
    <div className="p-3 border rounded bg-white shadow">
      <p className="mb-2">{text}</p>
      <button onClick={onConfirm} className="px-3 py-1 rounded bg-black text-white">Confirmar</button>
    </div>
  );
}
