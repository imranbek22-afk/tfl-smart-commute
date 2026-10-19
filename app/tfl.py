"""
TfL API helpers.
"""

from typing import Any

import httpx

BASE_URL = "https://api.tfl.gov.uk"
DEFAULT_MODES = ["tube", "overground", "dlr", "elizabeth-line"]
TIMEOUT = 8.0  # seconds — fail reasonably fast if TfL is slow


class TfLError(Exception):
    """Base exception for TfL API problems."""

    def __init__(self, message: str, user_message: str | None = None):
        super().__init__(message)
        self.user_message = user_message or message


class TfLTimeoutError(TfLError):
    """Raised when the TfL API does not respond in time."""


class TfLUnavailableError(TfLError):
    """Raised when the TfL API is unreachable or returns an error status."""


async def get_line_statuses(modes: list[str] | None = None) -> list[dict[str, Any]]:
    """Fetch live line statuses for the given modes (or default rail modes).

    Supports Tube, Overground, DLR and Elizabeth line by default.

    Args:
        modes: List of TfL mode names (e.g. ["tube", "dlr"]). Defaults to
            the main rail modes used by the app.

    Returns:
        List of line objects (each with lineStatuses) from the TfL API.

    Raises:
        TfLTimeoutError: If the request times out.
        TfLUnavailableError: On network errors or non-success HTTP status.
        TfLError: On unexpected response shapes.
    """
    if modes is None:
        modes = DEFAULT_MODES

    modes_param = ",".join(modes)
    url = f"{BASE_URL}/Line/Mode/{modes_param}/Status"

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
    except httpx.TimeoutException as exc:
        raise TfLTimeoutError(
            "TfL API request timed out",
            "The TfL service is taking too long to respond. Please try again in a moment.",
        ) from exc
    except httpx.HTTPStatusError as exc:
        raise TfLUnavailableError(
            f"TfL API returned {exc.response.status_code}",
            "The TfL service is temporarily unavailable. Please try again shortly.",
        ) from exc
    except httpx.RequestError as exc:
        raise TfLUnavailableError(
            f"Network error contacting TfL: {exc}",
            "We couldn't reach the TfL service. Please check your connection and try again.",
        ) from exc
    except ValueError as exc:
        # Invalid JSON
        raise TfLError(
            "Invalid response from TfL API",
            "Received an unexpected response from TfL. Please try again later.",
        ) from exc

    if not isinstance(data, list):
        raise TfLError(
            "Unexpected response shape from TfL API",
            "Received an unexpected response from TfL. Please try again later.",
        )

    return data
