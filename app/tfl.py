"""
TfL API helpers.
"""

import httpx

BASE_URL = "https://api.tfl.gov.uk"


async def get_line_statuses() -> list:
    """Fetch live status for Tube, Elizabeth line, DLR and Overground.

    Returns the raw JSON list from the TfL Unified API.
    """
    url = f"{BASE_URL}/Line/Mode/tube,elizabeth-line,dlr,overground/Status"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
