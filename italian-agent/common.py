"""
Shared utilities for all Italian lesson extraction agents.
"""

import json
import os
import sys

from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, set_default_openai_key

from pdf_utils import extract_pdf_text_with_pages, infer_unit_number

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL = "gpt-5.4"

if OPENAI_API_KEY:
    set_default_openai_key(OPENAI_API_KEY)


# ─── Globals set per-run ─────────────────────────────────────────────────────

_current_pdf_text: str = ""
_current_unit_number: int = 1
_output_dir: str = "output"
_saved_lessons: list[str] = []


# ─── Tools ───────────────────────────────────────────────────────────────────

@function_tool
def get_unit_text() -> str:
    """Returns the full PDF text with [PAGE X] markers."""
    return _current_pdf_text


@function_tool
def get_unit_number() -> int:
    """Returns the current unit number being processed."""
    return _current_unit_number


@function_tool
def save_extracted_lessons(lessons_json: str) -> str:
    """
    Saves extracted lesson JSON objects to disk.

    Args:
        lessons_json: A JSON string — either an array [{...}, ...] or a single object {...}.

    Returns:
        Confirmation message with saved filenames.
    """
    global _saved_lessons

    try:
        data = json.loads(lessons_json)
    except json.JSONDecodeError as e:
        return f"ERROR: Invalid JSON — {e}"

    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list):
        return "ERROR: Expected a JSON array or object."

    saved = []
    for lesson in data:
        title = lesson.get("title", f"lesson_{len(_saved_lessons) + 1}")
        filepath = os.path.join(_output_dir, f"{title}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(lesson, f, indent=2, ensure_ascii=False)
        _saved_lessons.append(filepath)
        saved.append(os.path.basename(filepath))
        print(f"  Saved: {filepath}")

    return f"Saved {len(saved)} lesson(s): {', '.join(saved)}"


TOOLS = [get_unit_text, get_unit_number, save_extracted_lessons]


# ─── Runner ──────────────────────────────────────────────────────────────────

def run_agent(agent: Agent, pdf_path: str, unit_number: int | None, output_base: str) -> None:
    global _current_pdf_text, _current_unit_number, _output_dir, _saved_lessons

    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY not set in .env")
        sys.exit(1)

    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF not found: {pdf_path}")
        sys.exit(1)

    if unit_number is None:
        unit_number = infer_unit_number(pdf_path)

    _current_pdf_text = extract_pdf_text_with_pages(pdf_path)
    _current_unit_number = unit_number
    _output_dir = os.path.join(output_base, f"Unit {unit_number} JSON")
    _saved_lessons = []

    os.makedirs(_output_dir, exist_ok=True)

    print(f"PDF      : {pdf_path}")
    print(f"Unit     : {unit_number}")
    print(f"Pages    : {_current_pdf_text.count('[PAGE ')}")
    print(f"Output   : {_output_dir}")
    print("Running agent...\n")

    Runner.run_sync(agent, "Extract the lesson from the current PDF and save it.", max_turns=30)

    print(f"Lessons saved: {len(_saved_lessons)}\n")


def run_agent_on_dir(agent: Agent, pdf_dir: str, output_base: str) -> None:
    """Process every PDF in pdf_dir one by one, sorted by filename."""
    if not os.path.isdir(pdf_dir):
        print(f"ERROR: Directory not found: {pdf_dir}")
        sys.exit(1)

    pdfs = sorted(
        os.path.join(pdf_dir, f)
        for f in os.listdir(pdf_dir)
        if f.lower().endswith(".pdf")
    )

    if not pdfs:
        print(f"ERROR: No PDF files found in {pdf_dir}")
        sys.exit(1)

    print(f"Found {len(pdfs)} PDF(s) in {pdf_dir}\n{'─' * 50}")

    for i, pdf_path in enumerate(pdfs, start=1):
        print(f"\n[{i}/{len(pdfs)}] {os.path.basename(pdf_path)}")
        run_agent(agent, pdf_path, unit_number=None, output_base=output_base)

    print(f"{'─' * 50}\nAll done. Processed {len(pdfs)} file(s).")


# ─── CLI arg parser ──────────────────────────────────────────────────────────

def make_arg_parser(description: str):
    import argparse
    parser = argparse.ArgumentParser(description=description)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pdf", help="Path to a single unit PDF")
    group.add_argument("--dir", help="Directory containing multiple unit PDFs (processed in filename order)")
    parser.add_argument("--unit", type=int, default=None, help="Unit number — only used with --pdf (auto-detected if omitted)")
    parser.add_argument("--out", default="output", help="Base output directory (default: output/)")
    return parser


def run_from_args(agent: Agent, args) -> None:
    """Dispatch to single-file or directory mode based on parsed args."""
    if args.dir:
        run_agent_on_dir(agent, args.dir, args.out)
    else:
        run_agent(agent, args.pdf, args.unit, args.out)
