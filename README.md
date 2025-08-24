# Knotch Take Home Challenge - Daven Boparai

This full-stack application consists of a **backend (FastAPI, PostgreSQL)** and a **frontend (React, TypeScript)**.
Its goal is to display and interact with performance data for content items.

I have combined the frontend and backend READMEs into this single document, though you can still view them individually in their respective files if needed.

# Core Features

This application successfully implements all core features:

1. **Leaderboard Table View**

2. **Filtering & Sorting**

   - Text-based filtering (case-insensitive) on both _title_ and _URL_
   - Sorting by _title_ and _publish_date_ (ascending and descending) via API parameters

3. **Infinite Scroll Pagination**
   - Implemented with _IntersectionObserver_, fully compatible with filtering and sorting.

# Nice-to-Haves

This application also implements most of the nice-to-have features:

1. **Authentication**

   - Routes are protected using **Bearer Token authentication**.
   - Users can be created via `POST /api/register`.
   - Access tokens can be retrieved via `POST /api/login`.
   - Certain API routes, such as creating and updating content (`POST /api/content` and `PUT /api/content/{ID}`), require authentication.
   - Authentication for these routes was not wired in the frontend due to time constraints. With a bit more time, I would have added token storage and an Auth Provider to the application.

2. **Column Display Configurability (show/hide)**
   - Users can opt to show and hide columns in the frontend.
   - This will not trigger infinite scroll if no columns are displayed.
3. **Apply Filters Button**
   - Users can enter filter values in the search bar.
   - When **Apply Filters Mode** is enabled, filters are only applied after clicking the **Apply Filters** button.
   - When the mode is disabled, input changes immediately update the data.
   - _Future Enhancement:_ Support for **debounced search** to improve performance and user experience.

# API Overview

This is also accessible at http://127.0.0.1:8000/docs

1. **Authentication-Related**

   - `GET /api/me` - To retrieve a user given an Auth Bearer Token
   - `POST /api/register` - To register a new user with a username, password JSON body supplied.
   - `POST /api/login` - To login a user with a username, password Form URL Encoded params.

2. **Content-Related**
   - `GET /api/content` - To retrieve content items with URL Params (search, sort_field, sort_order, limit, cursor)
   - `GET /api/content/{ID}` - To retrieve a specific content item
   - `PUT /api/content/{ID}` - To update a specific content item (_Requires Auth_)
   - `DELETE /api/content/{ID}` - To delete a specific content item (_Requires Auth_)
   - `POST /api/content` - To create a new content item (_Requires Auth_)

## Project Structure

```
content-leaderboard
├── backend
│   ├── README.md
└── frontend
    ├── README.md
```

## Requirements

- **Backend**: Python 3.13 (see [backend/README.md](backend/README.md))
- **Frontend**: Node.js 22+ and npm (see [frontend/README.md](frontend/README.md))

## Quick Start (Backend)

### 1. Configure Environment (Mac OS)

**Create a `.env` file with**

- ```
  DATABASE_URL=postgresql://[username]:[password]@localhost:5432/content_leaderboard
  SECRET_KEY=KNOTCHPROJECT
  ```

### 2. Installation and Run

**Create Virtual Environment for Python**

- ```
      python -m venv .venv
      source .venv/bin/activate
  ```

**Install Dependencies**

- ```
      pip install -r requirements.txt
  ```

**Ensure Database Exists**

- ```
    createdb content_leaderboard
    # You made need to use -U to specify a user
  ```

**Seed Data to DB via PSQL**

- ```
  # You made need to use -U to specify a user
  # Alternatively, this can be done in PgAdmin.

  psql -U postgres -d content_leaderboard < seed_data.sql
  ```

**Run the API from app folder**

- ```
  cd app
  uvicorn main:app --reload
  ```

API is accessible at **http://127.0.0.1:8000/**

Open **http://127.0.0.1:8000/docs** for Interactive Swagger docs.

## Quick Start (Frontend)

### 1. Configure Environment (Mac OS)

**Create a `.env` file at root with**

```
  API_BASE=http://127.0.0.1:8000
  # Or use your own
```

### 2.) Installation and Run

**Install Dependencies** (Node v22.14.0, npm 11.2.0)

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

### 1. Cursor (Key-Set) Pagination

**Decision**: Use Cursor Pagination over Offset/Limit Pagination.

**Rationale**:

- **Performance:** Cursor pagination can quickly query the next set of data using indexes whereas offset/limit pagination has to scan and discard rows with larger offsets.
- **Data Consistency:** Limit/Offset is prone to drifting data when rows are deleted or changed during browsing in a table.
  - Example: If a user is viewing records 1-10, and record 10 is deleted before they request the next page, the database will return what was originally record 11 as part of a new records 10-20. This causes a duplicate for whatever record 10 is supposed to be. It will appear in both pages.
- **Deterministic Ordering:** Using a row ID and sort_field value, we can achieve a stable ordering and traversal for pagination

**Trade-Offs**:

- **Complexity**: Takes longer to implement over Offset/Limit Pagination because of cursor encoding of id and sort_field value and dealing with tie breakers.
- **Stateful navigation**: Cursor Pagination is stateful. A client needs to hold onto a cursor to fetch the next page.
- **No random page access**: Unlike offset/limit, you can't jump to a certain page using offset/limit. You need a cursor and need to sequentially navigate through it.

### 2. Indexing in Content table

**Decision**: Add index on url, title, id, lower(title), lower(url) for content table.

**Rationale**:

- **Performance**: By indexing lower(title) and lower(url) we're able to search/filter results by these fields a lot quicker.
- **Cursor Pagination Requirement** Sorting/filtering by indexed fields is fast and predictable.

**Trade-Offs**:

- More indexes increase disk storage but this is acceptable given this a read-heavy app.

### 3. Leaderboard Hook

**Decision**: Use a custom leaderboard hook (useLeaderboard) to encapsulate loading state, error handling and fetching of data.

**Rationale**:

- Encapsulates all data fetching logic in one place, keeping App.jsx and LeaderboardTable focused on presentation.

**Trade Offs**:

- No caching between components, a shared state manager might be a better approach.

### 4. Search UX

**Decision**: Implement Two Modes for Search (Live and Apply Filters) Separately.

**Rationale**:

- Instant mode: Best for exploratory, instant feedback
- Apply mode: Avoids excessive queries to backend by requiring the user to explicitly trigger a new search.

**Trade-Offs**:

- **Complexity**: Both implementations have to be maintained in parellel

## Assumptions Taken

### Backend

- I assumed that this was a leaderboard app for one team/company and this was an internal tool to track analytics data. To incorporate this for a larger scale where more groups can access their own data via login/register requires a bit of a re-write.
- Metrics might change often, so cursor pagination is preferred for data consistency.
- Valid publish_date is inbetween January 1, 1990 and today's date.
- Page View, click_count, conversion_count must be positive integers.
- Urls must be unique

### Frontend

- Don't rely on external dependencies like Tanstack Table/Query
- Optimized for datasets <10k rows, so memoization via useMemo was not used

## Future Enhancements

### Backend

- Caching
- Rate Limiting
- Logging queries
- Sentry Integration for errors
- Wide Test Coverage. Testing all CRUD operations.
- More substantial User Model (emails)

### Frontend

- Testing (component, hook and e2e tests)
- TypeScript Types (strict mode is currently off)
- Routes via React Router
- Implementing Debounced Search
- Using TanStack Library for Querying and Table
- Sticky Header
- Back to Top button
