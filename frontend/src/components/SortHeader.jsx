export default function SortHeader({
  label,
  field,
  sortBy,
  sortOrder,
  onSort,
}) {
  const active = sortBy === field;
  const nextDir = !active ? "asc" : sortOrder === "asc" ? "desc" : "asc";
  const arrow = !active ? "" : sortOrder === "asc" ? "▲" : "▼";
  return (
    <button
      className={`th clickable ${active ? "active" : ""}`}
      onClick={() => onSort(field, nextDir)}
    >
      {label} {arrow}
    </button>
  );
}
