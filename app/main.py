from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.tfl import get_line_statuses, TfLError, TfLTimeoutError, TfLUnavailableError

app = FastAPI(title="TfL Smart Commute")
templates = Jinja2Templates(directory="app/templates")


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
        },
    )
