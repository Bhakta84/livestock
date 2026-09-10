# BLDCL Google Sheets e-Procurement Setup

## 1. Create storage
Create:
1. A Google Sheet for the application database.
2. A Google Drive folder for tender and bid files.

## 2. Apps Script
Open the Google Sheet -> Extensions -> Apps Script.
Copy `google-apps-script/Code.gs`.
Replace:
- `PASTE_GOOGLE_SHEET_ID_HERE`
- `PASTE_GOOGLE_DRIVE_FOLDER_ID_HERE`

Run `setup()` once and authorize the script.

## 3. Deploy API
Deploy -> New deployment -> Web app.
- Execute as: Me
- Access: your BLDCL Google Workspace users, or Anyone with the link if external bidders must register.

Copy the Web App URL.

## 4. Connect React
Open `frontend/src/googleSheetApi.js` and replace:
`PASTE_YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL_HERE`
with the Web App URL.

## 5. Start React
```bash
cd frontend
npm install
npm run dev
```

## Workflow now connected
Bidder Registration
-> Login
-> Tender List
-> Tender Details
-> Tender Documents (Google Drive)
-> Participate
-> BOQ Rate Entry
-> Save BOQ
-> Upload Bid Document to Drive
-> Submit Bid
-> Bid Receipt / Reference

Google Sheet tabs created by setup:
Users, Tenders, Documents, BOQs, BOQ_Items, Bids, Bid_Items, AuditLog.

Important:
This is a functional prototype. For production procurement, add stronger identity verification,
server-side access controls for Drive files, formal encryption/sealed-bid handling, email delivery,
rate/quantity validation, committee workflow, immutable audit controls, backups, and security testing.
