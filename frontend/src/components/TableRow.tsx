export default function TableRow({ row, visibleColumns }) {
  return (
    <tr>
      {visibleColumns.map((column) => (
        <td key={`${row.id}-${column.key}`}>
          {column.key === "url" ? (
            <a href={row[column.key]} target="_blank" rel="noreferrer">
              {row[column.key]}
            </a>
          ) : column.key === "publish_date" ? (
            new Date(row.publish_date).toLocaleString("en-US", {
              year: "numeric",
              month: "short",
              day: "numeric",
              hour: "2-digit",
              minute: "2-digit",
              second: "2-digit",
            })
          ) : (
            String(row[column.key])
          )}
        </td>
      ))}
    </tr>
  );
}
