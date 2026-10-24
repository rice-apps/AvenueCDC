"""Print the full ElevenLabs record for the most recent completed call."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ELEVENLABS_CONVERSATIONS_URL = (
    "https://api.elevenlabs.io/v1/convai/conversations"
)
PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ElevenLabsError(RuntimeError):
    """Raised when ElevenLabs cannot return the requested conversation."""


def load_local_env(path: Path = PROJECT_ROOT / ".env") -> None:
    """Load simple KEY=VALUE entries without overriding existing environment values.

    This intentionally small loader is enough for the project's current `.env` file
    and avoids adding a dependency for the initial API experiment.
    """

    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith("#"):
            continue

        key, separator, value = stripped_line.partition("=")
        if not separator:
            continue

        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]

        if key:
            os.environ.setdefault(key, value)


def request_json(url: str, api_key: str, timeout_seconds: float = 20.0) -> dict[str, Any]:
    """Send an authenticated GET request and return its decoded JSON object."""

    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "xi-api-key": api_key,
        },
        method="GET",
    )

    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            payload = json.load(response)
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise ElevenLabsError(
            f"ElevenLabs returned HTTP {error.code}: {detail}"
        ) from error
    except URLError as error:
        raise ElevenLabsError(f"Could not reach ElevenLabs: {error.reason}") from error
    except json.JSONDecodeError as error:
        raise ElevenLabsError("ElevenLabs returned invalid JSON.") from error

    if not isinstance(payload, dict):
        raise ElevenLabsError("ElevenLabs returned an unexpected response shape.")

    return payload


def get_most_recent_call(
    api_key: str,
    agent_id: str,
    timeout_seconds: float = 20.0,
) -> dict[str, Any] | None:
    """Return full details for the agent's newest completed conversation.

    Conversations still being handled or analyzed are excluded so that transcript
    and post-call analysis fields have had time to finish processing.
    """

    query = urlencode(
        [
            ("agent_id", agent_id),
            ("page_size", "1"),
            ("sort_direction", "desc"),
            ("exclude_statuses", "initiated"),
            ("exclude_statuses", "in-progress"),
            ("exclude_statuses", "processing"),
            ("exclude_statuses", "failed"),
        ]
    )
    conversation_list = request_json(
        f"{ELEVENLABS_CONVERSATIONS_URL}?{query}",
        api_key,
        timeout_seconds,
    )

    conversations = conversation_list.get("conversations")
    if not isinstance(conversations, list):
        raise ElevenLabsError("The conversation list response is missing 'conversations'.")
    if not conversations:
        return None

    latest_conversation = conversations[0]
    if not isinstance(latest_conversation, dict):
        raise ElevenLabsError("The latest conversation has an unexpected shape.")

    conversation_id = latest_conversation.get("conversation_id")
    if not isinstance(conversation_id, str) or not conversation_id:
        raise ElevenLabsError("The latest conversation is missing its conversation ID.")

    return request_json(
        f"{ELEVENLABS_CONVERSATIONS_URL}/{conversation_id}",
        api_key,
        timeout_seconds,
    )


def main() -> int:
    """Load local configuration and print the latest completed call as JSON."""

    load_local_env()
    api_key = os.getenv("ELEVENLABS_API")
    agent_id = os.getenv("ELEVENLABS_AGENT_ID")

    missing_variables = [
        name
        for name, value in (
            ("ELEVENLABS_API", api_key),
            ("ELEVENLABS_AGENT_ID", agent_id),
        )
        if not value
    ]
    if missing_variables:
        print(
            f"Missing required environment variable(s): {', '.join(missing_variables)}",
            file=sys.stderr,
        )
        return 1

    try:
        conversation = get_most_recent_call(api_key, agent_id)
    except ElevenLabsError as error:
        print(f"Unable to retrieve the latest call: {error}", file=sys.stderr)
        return 1

    if conversation is None:
        print("No completed conversations were found for this agent.", file=sys.stderr)
        return 1

    json.dump(conversation, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
