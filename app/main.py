from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.tfl import get_line_statuses

app = FastAPI(title="TfL Smart Commute")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        lines = await get_line_statuses()
    except Exception as e:
        lines = []
        error = str(e)
    else:
        error = None

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "lines": lines,
            "error": error,
        }
    )
