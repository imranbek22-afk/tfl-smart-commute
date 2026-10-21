from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.tfl import get_line_statuses, TfLError, TfLTimeoutError, TfLUnavailableError

app = FastAPI(title="TfL Smart Commute")
templates = Jinja2Templates(directory="app/templates")

# Simple in-memory store for journeys (resets on restart)
journeys: list[dict] = []


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    lines: list = []
    error: str | None = None

    try:
        lines = await get_line_statuses()
    except TfLTimeoutError as e:
        error = e.user_message
    except TfLUnavailableError as e:
        error = e.user_message
    except TfLError as e:
        error = e.user_message
    except Exception:
        # Catch-all so the page never crashes
        error = "Something went wrong while fetching line statuses. Please try again later."

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "lines": lines,
            "error": error,
            "journeys": journeys,
        },
    )


@app.post("/add-journey")
async def add_journey(
    name: str = Form(...),
    origin: str = Form(...),
    destination: str = Form(...),
    lines: str = Form(""),
):
    """Store a new journey in memory."""
    journey = {
        "name": name.strip(),
        "origin": origin.strip(),
        "destination": destination.strip(),
        "lines": [line.strip() for line in lines.split(",") if line.strip()],
    }
    journeys.append(journey)
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete-journey")
async def delete_journey(index: int = Form(...)):
    """Remove a journey from memory by its list index."""
    try:
        if 0 <= index < len(journeys):
            journeys.pop(index)
    except (ValueError, IndexError):
        pass  # Ignore invalid indices
    return RedirectResponse(url="/", status_code=303)
