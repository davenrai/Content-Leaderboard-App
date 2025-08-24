export default function ColumnPicker({ columns, onToggle }) {
  return (
    <div className="column-picker">
      {columns.map((col) => (
        <label key={col.key} className="chip">
          <input
            type="checkbox"
            checked={!col.hidden}
            onChange={() => onToggle(col.key)}
          />
          {col.label}
        </label>
      ))}
    </div>
  );
}
