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
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
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

For production, change the demo password, configure PostgreSQL, HTTPS,
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
