import { useState } from "react";
import LeaderboardTable from "./components/LeaderboardTable";
import ColumnPicker from "./components/ColumnPicker";
import { useLeaderboard } from "./hooks/useLeaderboard";

export default function App() {
  const [search, setSearch] = useState("");
  const [draftSearch, setDraftSearch] = useState("");
  const [applyMode, setApplyMode] = useState(true);
  const [applyTrigger, setApplyTrigger] = useState(0);

  const [sortField, setSortField] = useState("publish_date");
  const [sortOrder, setSortOrder] = useState("desc");

  const [columns, setColumns] = useState([
    { key: "title", label: "Title", sortable: true, hidden: false },
    { key: "url", label: "URL", sortable: false, hidden: false },
    {
      key: "publish_date",
      label: "Publish Date",
      sortable: true,
      hidden: false,
    },
    {
      key: "page_view_count",
      label: "Page Views",
      sortable: false,
      hidden: false,
    },
    {
      key: "click_count",
      label: "Clicks",
      sortable: false,
      hidden: false,
    },
    {
      key: "conversion_count",
      label: "Conversions",
      sortable: false,
      hidden: false,
    },
    {
      key: "average_scroll_depth",
      label: "Avg Scroll %",
      sortable: false,
      hidden: false,
    },
  ]);

  const toggleCol = (key) => {
    setColumns((cols) =>
      cols.map((c) => (c.key === key ? { ...c, hidden: !c.hidden } : c))
    );
  };

  const { items, loadMore, loading, error, hasMore } = useLeaderboard({
    searchInput: search,
    sortField: sortField,
    sortOrder: sortOrder,
    applyMode,
    applyTrigger,
  });

  const onSort = (field, order) => {
    setSortField(field);
    setSortOrder(order);
  };

  const onApply = () => {
    setSearch(draftSearch.trim());
    setApplyTrigger((t) => t + 1);
  };

  return (
    <div className="container">
      <header>
        <h1>Content Leaderboard</h1>
      </header>

      <section className="controls">
        <div className="search">
          {applyMode ? (
            <>
              <input
                value={draftSearch}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    onApply();
                  }
                }}
                onChange={(e) => setDraftSearch(e.target.value)}
                placeholder="Filter by title or URL"
              />
              <button onClick={onApply}>Apply Filters</button>
            </>
          ) : (
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Filter by title or URL"
            />
          )}
          <button
            onClick={() => {
              setDraftSearch("");
              setSearch("");
            }}
          >
            Clear Filter
          </button>
        </div>
        <div className="toggles">
          <label className="chip">
            <input
              type="checkbox"
              checked={applyMode}
              onChange={(e) => setApplyMode(e.target.checked)}
            />
            Apply Filters Mode
          </label>
        </div>
        <ColumnPicker columns={columns} onToggle={toggleCol} />
      </section>
      {!error ? (
        <LeaderboardTable
          items={items}
          onLoadMore={loadMore}
          hasMore={hasMore}
          loading={loading}
          sortBy={sortField}
          sortOrder={sortOrder}
          onSort={onSort}
          columns={columns}
        />
      ) : (
        <p>{String(error)}</p>
      )}
    </div>
  );
}
