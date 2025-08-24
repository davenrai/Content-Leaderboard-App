const API = import.meta.env.API_BASE || "http://127.0.0.1:8000";
const ENDPOINT = `${API}/api/content`;

export async function fetchContent({
  searchInput,
  limit,
  sortOrder,
  sortField,
  cursor,
}) {
  const params = new URLSearchParams();
  if (searchInput) params.set("search", searchInput);
  if (sortOrder) params.set("sort_order", sortOrder);
  if (sortField) params.set("sort_field", sortField);
  if (limit) params.set("limit", String(limit));
  if (cursor) params.set("cursor", cursor);

  const res = await fetch(`${ENDPOINT}?${params.toString()}`);
  if (!res.ok) throw new Error(`HTTP ERROR: ${res.status}`);
  return res.json();
}
