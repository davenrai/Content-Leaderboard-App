# Knotch Backend

This backend implements the server side for the take home challenge: Content Leaderboard App. Built by Daven Boparai.

## Tech Stack

- **Python 3.13**
- **FastAPI 0.116.1**
- **PostGreSQL 17**

## Quick Start (Backend)

### 1. Configure Environment (Mac OS)

```
cd backend
```

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

**Run the API from app folder (Creates tables)**

- ```
  cd app
  uvicorn main:app --reload
  ```

**Seed Data to DB via PSQL**

- ```
  # You made need to use -U to specify a user
  # Alternatively, this can be done in PgAdmin.

  psql -U postgres -d content_leaderboard < seed_data.sql
  ```

API is accessible at **http://127.0.0.1:8000/**

Open **http://127.0.0.1:8000/docs** for Interactive Swagger docs.

### Health

- `GET /api` - returns message ensuring API is up and running.

## Design Decisions

### Cursor (Key-Set) Pagination

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

### Indexing in Content table

**Decision**: Add index on url, title, id, lower(title), lower(url) for content table.

**Rationale**:

- **Performance**: By indexing lower(title) and lower(url) we're able to search/filter results by these fields a lot quicker.
- **Cursor Pagination Requirement** Sorting/filtering by indexed fields is fast and predictable.

**Trade-Offs**:

- More indexes increase disk storage but this is acceptable given this a read-heavy app.

## Assumptions Taken

- I assumed that this was a leaderboard app for one team/company and this was an internal tool to track analytics data. To incorporate this for a larger scale where more groups can access their own data via login/register requires a bit of a re-write.
- Valid publish_date is in-between January 1, 1990 and today's date.
- Page View, click_count, conversion_count must be positive integers.
- Urls must be unique

## Future Enhancements

- Caching
- Rate Limiting
- Logging queries
- Sentry Integration for errors
- Test Coverage. Testing all crud operations
- More substantial User Model (emails)
