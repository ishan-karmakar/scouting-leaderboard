# Leaderboard Flask App

A Flask application that fetches leaderboard data from a Google Sheet and displays it in a web interface.

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Google Credentials
Ensure `credentials.json` is in the root directory with your Google service account credentials.

## Running the App

```bash
python app.py
```

The app will start on `http://localhost:5000`

## How It Works

1. **Frontend** (`templates/leaderboard.html`):
   - Displays a styled leaderboard page
   - Fetches data from the API endpoint
   - Refreshes every 30 seconds
   - Highlights top 3 positions

2. **Backend** (`app.py`):
   - Authenticates with Google Sheets API using credentials.json
   - Reads from the "Aura Override" sheet
   - Extracts data from "Scouts" (names) and "Aura" (scores) columns
   - Sorts by score (highest first)
   - Provides two routes:
     - `GET /` - Serves the leaderboard page
     - `GET /api/leaderboard` - Returns JSON array of leaderboard entries

## API Response

The `/api/leaderboard` endpoint returns JSON in this format:

```json
[
  {
    "name": "Scout Name",
    "score": 100.5
  },
  ...
]
```

Data is sorted by score in descending order.
