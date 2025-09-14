# Client Query Management System (Streamlit)

A lightweight ticketing app for collecting client issues and managing them from a Support dashboard.  
Built with **Streamlit + SQLite** (single folder, no external services).

---

## ✨ Features

- **Landing page** with live ticker, flash cards, donut chart, and 14-day trend
- **Clients** submit tickets (email/phone, heading, description, optional screenshot)
- **Support Dashboard**
  - View / search / filter (All • Open • In Progress • Closed) + date range
  - Set status to **In Progress** or **Closed** (single or **bulk** close)
  - View attached screenshots
  - Add/read **internal notes** per ticket
  - Download **filtered CSV**
  - Mini donut chart for current filter
- **Auth**: username/password with role (**Client** or **Support**)
- **Data**: local `app.db` (SQLite) seeded from `data/seed_queries.csv`

---

## 📦 Project Structure

client-query-management-system/
├─ app.py
├─ auth.py
├─ db.py
├─ requirements.txt
├─ .streamlit/
│ └─ config.toml
├─ data/
│ └─ seed_queries.csv
├─ pages/
│ ├─ 1_Client_Submission.py
│ └─ 2_Support_Dashboard.py
└─ assets

---

## 🚀 Quick Start

# 1) Clone
git clone <YOUR-REPO-URL>
cd client-query-management-system

# 2) Virtual env
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 3) Install
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 4) Run
python -m streamlit run app.py

Open http://localhost:8501

🔐 First Use

In the sidebar, Register a user (choose role: Client or Support).

Switch to Login and sign in.

Use the sidebar links to open Client Submission or Support Dashboard.

The first run auto-loads seed tickets from data/seed_queries.csv.

🧭 How to Use

Client Submission

Fill Email, Mobile, Heading, Description

Optionally attach a screenshot

Submit → ticket starts as Open

Support Dashboard

Filter by Status (All / Open / In Progress / Closed), Search, and Date range

In Progress: enter ID → Mark In Progress

Close: enter ID → Mark Closed (writes close timestamp)

Bulk Close: pick multiple IDs from the table → Bulk Close Selected

Notes: add internal notes for a ticket (stored in SQLite)

View Image: load details for an ID to see its screenshot

Export: Download filtered CSV

🗄️ Data & Reset

App database: app.db in project root (SQLite)

To reset: stop Streamlit, delete app.db, start the app (seed data reloads)

🛠️ Troubleshooting

pandas / build errors on Windows

python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
# if needed:
pip install --only-binary=:all: pandas==2.2.2


ModuleNotFoundError: matplotlib

pip install matplotlib


Port already in use

streamlit run app.py --server.port 8502

☁️ Deploy (Streamlit Community Cloud)

Push this repo to GitHub.

Go to https://share.streamlit.io
 → New app → connect your repo.

Main file path: app.py.

Ensure requirements.txt is present. Deploy.

🎨 Customize

Theme: .streamlit/config.toml

Seed data: data/seed_queries.csv

Landing (metrics/cards/charts): app.py

Support features (filters, notes, bulk actions): pages/2_Support_Dashboard.py

DB logic/schema: db.py

## Problem Statement
Build a Client Query Management System that allows:
- Clients to submit issues (email/phone, heading, description, optional screenshot)
- Support to view, search, filter (All/Open/In Progress/Closed), update status, add internal notes, and export CSV
- Basic analytics on the landing page (live counts, donut of Open vs Closed, 14-day trend)
- Local persistence using SQLite with seed data
- Simple auth with roles (Client/Support)

Deliverables: working Streamlit app, source code on GitHub, README with setup, and deployed Streamlit Cloud URL.

📄 License

MIT — free to use and modify for coursework and demos.


If you want a minimal badge/header section or your name/college added at the top, tell me the details and I’ll slot them in.
