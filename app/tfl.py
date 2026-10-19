"""
TfL API helpers.
"""

from typing import Any

import httpx

BASE_URL = "https://api.tfl.gov.uk"
DEFAULT_MODES = ["tube", "overground", "dlr", "elizabeth-line"]
TIMEOUT = 10.0


async def get_line_statuses(modes: list[str] | None = None) -> list[dict[str, Any]]:
    """Fetch live line statuses for the given modes (or default rail modes).

    Supports Tube, Overground, DLR and Elizabeth line by default.

    Args:
        modes: List of TfL mode names (e.g. ["tube", "dlr"]). Defaults to
            the main rail modes used by the app.

    Returns:
        List of line objects (each with lineStatuses) from the TfL API.

    Raises:
        httpx.HTTPStatusError: If the API returns a non-success status.
        httpx.RequestError: On network, timeout or other request failures.
    """
    if modes is None:
        modes = DEFAULT_MODES

    modes_param = ",".join(modes)
    url = f"{BASE_URL}/Line/Mode/{modes_param}/Status"

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
