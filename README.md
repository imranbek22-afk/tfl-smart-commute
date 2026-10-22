# TfL Smart Commute

A practical London commute companion built with **Python**, **FastAPI** and **Jinja2**.

This project helps you quickly see:
- Live status of London Underground, Overground, Elizabeth line and DLR
- Which of your saved journeys are currently affected by disruptions
- A simple "Is my commute okay?" overview

Built over several weeks as a personal tool I actually wanted to use.

## Features (planned / in progress)

- [x] Project structure and README
- [x] Live TfL line status (with clean summary + detailed list)
- [x] Filter: All lines / Disruptions only
- [x] Save and delete personal journeys (in-memory, displayed on the page)
- [x] Show live status for lines used by each saved journey
- [x] Clear indicator showing whether each saved journey is affected by disruptions
- [ ] Persistent storage with SQLite

## Tech Stack

- Python 3.11+
- FastAPI
- Jinja2 (HTML templates)
- SQLite (later)
- TfL Unified API

## Getting Started

```bash
git clone https://github.com/imranbek22-afk/tfl-smart-commute.git
cd tfl-smart-commute
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000

## Project Structure

```
tfl-smart-commute/
├── app/
│   ├── main.py
│   ├── tfl.py
│   └── templates/
├── requirements.txt
└── README.md
```

## Licence

Personal project / educational use.
