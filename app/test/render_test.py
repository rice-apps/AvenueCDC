import argparse
import json
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape


def load_call_data(json_path: Path) -> dict[str, Any]:
    """Load and validate a call record JSON object."""
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Could not read valid JSON from {json_path}: {error}") from error

    if not isinstance(data, dict):
        raise ValueError("The JSON document must contain an object at its top level.")
    return data


def render_call_report(call_data: dict[str, Any]) -> str:
    """Render call data into HTML using the local Jinja template."""
    template_directory = Path(__file__).parent
    environment = Environment(
        loader=FileSystemLoader(template_directory),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = environment.get_template("test.html")

    context = {
        "call_start": call_data.get("call_start", call_data.get("start")),
        "call_end": call_data.get("call_end", call_data.get("end")),
        "intake": call_data.get("intake", {}),
        "transcript": call_data.get("transcript"),
        "report": call_data.get("report"),
        "chat_session": call_data.get("chat_session"),
        "call_id": call_data.get("call_id"),
        "caller_number": call_data.get("caller_number"),
        "language": call_data.get("language"),
        "outcome": call_data.get("outcome"),
        "routed_to": call_data.get("routed_to"),
    }
    return template.render(**context)


def main() -> None:
    """Parse command-line arguments and write the rendered HTML report."""
    parser = argparse.ArgumentParser(
        description="Render a call record JSON file as an AvenueCDC HTML report."
    )
    parser.add_argument("json_file", type=Path, help="Path to the call record JSON file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output HTML path; print HTML to stdout when omitted",
    )
    args = parser.parse_args()

    html = render_call_report(load_call_data(args.json_file))
    if args.output:
        args.output.write_text(html, encoding="utf-8")
        print(f"Rendered report written to {args.output}")
    else:
        print(html)


if __name__ == "__main__":
    main()
