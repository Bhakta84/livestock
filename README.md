<<<<<<< HEAD
# BLDCL Online Tendering System

Working starter implementation:
- Backend: Django + Django REST Framework + JWT
- Database: PostgreSQL (SQLite fallback for local development)
- Frontend: React + Vite
- Storage: local media storage in development
- Roles: Admin, Procurement Officer, Evaluator, Approving Authority, Bidder

## Quick start

### Backend
```bash
cd backend
python manage.py runserver
```

API: http://127.0.0.1:8000/api/

Demo admin:
- username: admin
- password: Admin@12345

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173
email, and security settings before deployment.


## Google Sheets + Apps Script storage option

The `google-apps-script/` folder contains a Google Sheets database/API option.
Google Sheets stores tender, bid, user, document metadata, and audit records.
Google Drive stores the actual uploaded tender/bid files.

Setup:
1. Create a Google Sheet.
2. Create a Google Drive folder for tender/bid documents.
3. Put their IDs in `google-apps-script/Code.gs`.
4. Deploy the Apps Script as a Web App.
5. Put the Web App URL in `frontend/src/googleSheetApi.js`.

This removes the need for local media storage. The Django project is retained for the existing
authentication/API implementation; the Google Apps Script option is provided for sheet-based
data/document storage.
=======

# 🐷🐔 Livestock Information Dashboard

A comprehensive web-based dashboard for managing livestock information, specifically designed for tracking pigs and chicken egg production.

## Features

### 📊 Real-Time Statistics
- **Total Pigs Today**: Track pigs added for the current day
- **Total Eggs Today**: Track eggs collected for the current day
- **Total Pigs (All-time)**: Running total of all pigs recorded
- **Total Eggs (All-time)**: Running total of all eggs recorded

### 📝 Data Entry Forms
- **Add Pig Entry**: Enter number of pigs with optional notes
- **Add Egg Entry**: Enter number of eggs with optional notes
- Both forms support multiple entries per day
### 📋 Historical Data Tracking
- **Pig History Table**: Complete record of all pig entries with date, time, count, and notes
- **Egg History Table**: Complete record of all egg entries with date, time, count, and notes
- Delete individual entries as needed
- Tab-based navigation between pig and egg histories

### 💾 Data Management
- **Export to CSV**: Download all data in CSV format for external analysis
- **Clear All Data**: Remove all historical data (with confirmation)
- **Local Storage**: All data is automatically saved to browser's local storage

## How to Use

### Getting Started
1. Open `index.html` in your web browser
2. The dashboard will load with any previously saved data

2. Enter the number of pigs in the "Number of Pigs" field
3. Optionally add notes about the pigs (breed, health status, etc.)
4. Click "Add Pigs" button
5. Statistics will update automatically

### Adding Egg Entries
1. Navigate to the "Add Egg Entry" form on the right side
2. Enter the number of eggs collected in the "Number of Eggs" field
3. Optionally add notes about the collection (source, quality, etc.)
4. Click "Add Eggs" button
5. Statistics will update automatically

### Viewing Charts
- Charts automatically update after each entry
- Charts display data from the last 7 days
- Hover over data points for exact values
- Charts update in real-time (every 5 seconds)

### Reviewing History
1. Scroll to the "Historical Data" section
2. Click "Pig History" or "Egg History" tab
3. View all entries sorted by most recent first
4. Delete individual entries by clicking the "Delete" button

### Exporting Data
1. Scroll to the "Export Data" section at the bottom
2. Click "📥 Export to CSV" to download your data
3. File will be saved as `livestock-data-YYYY-MM-DD.csv`

### Clearing Data
1. Scroll to the "Export Data" section
2. Click "🗑️ Clear All Data"
3. Confirm the action when prompted
4. All historical data will be permanently deleted

## Features Details

### Real-Time Data Display
- Statistics refresh automatically every 5 seconds
- Charts update immediately after new entries
- No need to refresh the page manually

### Data Persistence
- All data is stored in browser's localStorage
- Data persists even after closing the browser
- Each browser/device maintains its own data

### Responsive Design
- Works on desktop, tablet, and mobile devices
- Adaptive grid layout for different screen sizes
- Touch-friendly interface on mobile devices

### Data Visualization Options
- Line charts for trend analysis (pigs)
- Bar charts for discrete data (eggs)
- Comparison charts for side-by-side analysis
- 7-day rolling window for data display

## Technical Stack

- **HTML5**: Semantic markup for dashboard structure
- **CSS3**: Responsive design with gradients and animations
- **JavaScript (Vanilla)**: No dependencies for data management
- **Chart.js**: Library for interactive charts and graphs
- **LocalStorage API**: Browser-based data persistence

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Data Storage

All data is stored locally in your browser using the LocalStorage API:
- `pigData`: Array of pig entries
- `eggData`: Array of egg entries

Each entry contains:
```javascript
{
  date: "YYYY-MM-DD",
  time: "HH:MM:SS",
  count: number,
  notes: string
}
```

## Keyboard Shortcuts

- **Ctrl+S** (or **Cmd+S** on Mac): Export data to CSV

## Tips for Best Use

1. **Regular Entries**: Add entries at consistent times daily for accurate tracking
2. **Detailed Notes**: Include useful notes (breed, health status, feeding changes, etc.)
3. **Regular Backups**: Export your data regularly to keep backups
4. **Data Review**: Check charts weekly to identify trends
5. **Mobile Access**: Access from any device with a web browser

## File Structure

```
livestock/
├── index.html      # Main HTML structure
├── styles.css      # CSS styling and responsive design
├── script.js       # JavaScript functionality
└── README.md       # Documentation (this file)
```

## Version

Version 1.0.0 - Initial Release

## Support

For issues or feature requests, please contact the development team.

---

Made with ❤️ for livestock management
>>>>>>> origin/main
