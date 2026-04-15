import os
import json
from flask import Flask, render_template, jsonify
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = os.getenv('GOOGLE_SHEETS_PIT_SPREADSHEET_ID')

def get_google_sheets_service():
    """Authenticate and return Google Sheets service."""
    creds = Credentials.from_service_account_file(
        'credentials.json',
        scopes=SCOPES
    )
    service = build('sheets', 'v4', credentials=creds)
    return service

def get_leaderboard_data():
    """Fetch leaderboard data from Google Sheets."""
    try:
        service = get_google_sheets_service()
        
        # Read from "Aura Override" sheet
        sheet_name = "Aura Override"
        range_name = f"'{sheet_name}'!A:Z"  # Read all columns
        
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            return []
        
        # Parse the header row to find column indices
        header = values[0]
        scouts_col = None
        aura_col = None
        
        for i, col_name in enumerate(header):
            if col_name.lower() == 'scouts':
                scouts_col = i
            elif col_name.lower() == 'aura':
                aura_col = i
        
        if scouts_col is None or aura_col is None:
            print(f"Could not find columns. Header: {header}")
            return []
        
        # Extract leaderboard data
        leaderboard = []
        for row in values[1:]:  # Skip header
            if len(row) > max(scouts_col, aura_col):
                name = row[scouts_col].strip() if scouts_col < len(row) else ""
                score_str = row[aura_col].strip() if aura_col < len(row) else ""
                
                # Skip empty rows
                if not name:
                    continue
                
                # Convert score to float, handle if it's not a number
                try:
                    score = float(score_str)
                except ValueError:
                    score = 0.0
                
                leaderboard.append({
                    'name': name,
                    'score': score
                })
        
        # Sort by score in descending order
        leaderboard.sort(key=lambda x: x['score'], reverse=True)
        
        return leaderboard
    
    except Exception as e:
        print(f"Error fetching leaderboard data: {e}")
        return []

@app.route('/')
def index():
    """Render the leaderboard page."""
    return render_template('leaderboard.html')

@app.route('/api/leaderboard')
def leaderboard_api():
    """API endpoint to get leaderboard data."""
    data = get_leaderboard_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run()
