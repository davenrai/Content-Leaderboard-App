import { useEffect, useRef } from "react";
import SortHeader from "./SortHeader";
import TableRow from "./TableRow";

export default function LeaderboardTable({
  items,
  onLoadMore,
  hasMore,
  loading,
  sortBy,
  sortOrder,
  onSort,
  columns,
}) {
  // For Infinite Scrolling
  const visibleCols = columns.filter((c) => !c.hidden);
  const sentinelRef = useRef(null);

  useEffect(() => {
    const el = sentinelRef.current;
    if (!el) return;
    const io = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && visibleCols.length > 0) {
          onLoadMore();
        }
      },
      { rootMargin: "500px", threshold: 1 }
    );
    io.observe(el);
    return () => io.disconnect();
  }, [onLoadMore]);

  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            {visibleCols.map((col) => (
              <th key={col.key} className="table-header">
                {col.sortable ? (
                  <SortHeader
                    label={col.label}
                    field={col.key}
                    sortBy={sortBy}
                    sortOrder={sortOrder}
                    onSort={onSort}
                  />
                ) : (
                  col.label
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {items.map((row) => (
            <TableRow key={row.id} row={row} visibleColumns={visibleCols} />
          ))}
        </tbody>
      </table>
      <div ref={sentinelRef} />
      {loading && <div className="loading">Loading…</div>}
      {visibleCols.length === 0 && (
        <div className="loading">No columns selected</div>
      )}
      {!hasMore && visibleCols.length > 0 && (
        <div className="end-table">No more results</div>
      )}
    </div>
  );
}
