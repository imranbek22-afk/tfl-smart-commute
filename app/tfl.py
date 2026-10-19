"""
TfL API helpers.
"""

import httpx

BASE_URL = "https://api.tfl.gov.uk"


# TODO: expand to elizabeth-line, dlr, overground once tube is solid
async def get_line_statuses():
    """Fetch live Tube line statuses (WIP - tube only for now).

    Returns the raw JSON list from the TfL API.
    """
    url = f"{BASE_URL}/Line/Mode/tube/Status"
    # rough for now - no timeout, basic error check
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            print(f"TfL request failed: {response.status_code}")
            return []  # TODO: raise properly later
        return response.json()
