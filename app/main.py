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
    request: Request,
    name: str = Form(...),
    origin: str = Form(...),
    destination: str = Form(...),
    lines: str = Form(""),
):
    """Store a new journey in memory with validation."""
    name = name.strip()
    origin = origin.strip()
    destination = destination.strip()
    lines_list = [line.strip() for line in lines.split(",") if line.strip()]

    form_errors: list[str] = []

    if len(name) < 2:
        form_errors.append("Journey name must be at least 2 characters.")
    if len(origin) < 2:
        form_errors.append("Origin must be at least 2 characters.")
    if len(destination) < 2:
        form_errors.append("Destination must be at least 2 characters.")
    if origin.lower() == destination.lower():
        form_errors.append("Origin and destination cannot be the same.")

    if form_errors:
        # Re-render the page with form errors and previous values
        lines_data: list = []
        error: str | None = None
        try:
            lines_data = await get_line_statuses()
        except (TfLTimeoutError, TfLUnavailableError, TfLError) as e:
            error = e.user_message
        except Exception:
            error = "Something went wrong while fetching line statuses. Please try again later."

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "lines": lines_data,
                "error": error,
                "journeys": journeys,
                "form_errors": form_errors,
                "form_data": {
                    "name": name,
                    "origin": origin,
                    "destination": destination,
                    "lines": lines,
                },
            },
            status_code=400,
        )

    journey = {
        "name": name,
        "origin": origin,
        "destination": destination,
        "lines": lines_list,
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
