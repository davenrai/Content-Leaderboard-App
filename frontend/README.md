# Knotch Frontend

This application implements the frontend for the take home challenge: Content Leaderboard App. Built by Daven Boparai.

## Tech Stack

- **React 19**
- **Vite**
- **TypeScript**
- **Node 22.14.0**

## Quick Start

### 1.) Configure Environment (Mac OS)

```
cd frontend
# You can also use the following (if you have Node Version Manager):
# nvm install 22.14.0
# nvm use 22.14.0
```

**Create a `.env` file at root with**

```
  API_BASE=http://127.0.0.1:8000
  # Or use your own
```

### 2.) Installation and Run

**Install Dependencies**

```
  npm ci
  npm install
```

**Run Application**

```
npm run dev
```

Open **http://localhost:5173/** for the frontend UI.

## Design Decisions

### Leaderboard Hook

**Decision**: Use a custom leaderboard hook (useLeaderboard) to encapsulate loading state, error handling and fetching of data.

**Rationale**:

- Encapsulates all data fetching logic in one place, keeping App.jsx and LeaderboardTable focused on presentation.

**Trade Offs**:

- No caching between components, a shared state manager might be a better approach.

### Search UX

**Decision**: Implement Two Modes for Search (Live and Apply Filters) Separately.

**Rationale**:

- Instant mode: Best for exploratory, instant feedback
- Apply mode: Avoids excessive queries to backend by requiring the user to explicitly trigger a new search.

**Trade-Offs**:

- **Complexity**: Both implementations have to be maintained in parellel

## Assumptions Taken

- Don't rely on dependencies like Tanstack table (don't think it supports cursor pagination)
- Stateless API, frontend client just displays data
- Auth is optional
- No major need to memoization (with useMemo) for columns because columns are inexpensive

## Future Enhancements

- Testing (component, hook and e2e tests)
- TypeScript Types (strict mode is currently off)
- Routes via React Router
- Implementing Debounced Search
- Using TanStack Library for Querying and Table
- Sticky Header
- Back to Top button
