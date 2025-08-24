import { useEffect, useState } from "react";
import { fetchContent } from "../api";

export function useLeaderboard({
  searchInput,
  sortField,
  sortOrder,
  applyMode,
  applyTrigger,
}) {
  const [items, setItems] = useState([]);
  const [cursor, setCursor] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasMore, setHasMore] = useState(true);

  useEffect(() => {
    setItems([]);
    setCursor(null);
    setHasMore(true);
  }, [searchInput, sortField, sortOrder, applyMode ? applyTrigger : null]);

  async function loadMore() {
    if (loading || !hasMore) return;
    setLoading(true);
    setError(null);
    try {
      const data = await fetchContent({
        searchInput,
        sortField,
        sortOrder,
        limit: 10,
        cursor,
      });
      setItems((prev) => [...prev, ...data.items]);
      setCursor(data.next_cursor || null);
      setHasMore(Boolean(data.next_cursor));
    } catch (e) {
      setError("Error: Unable to fetch data. Please verify the API is running");
    } finally {
      setLoading(false);
    }
  }

  return { items, loadMore, loading, error, hasMore };
}
