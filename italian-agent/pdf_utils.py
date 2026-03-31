import os
import re
from PyPDF2 import PdfReader

# Running headers/footers to strip from every page before sending to the agent.
_HEADERS_TO_STRIP = [
    r"ITALIAN FAST",
    r"Italian Fast",
]
_HEADER_PATTERN = re.compile(
    r"^\s*(?:" + "|".join(_HEADERS_TO_STRIP) + r")\s*$",
    re.MULTILINE | re.IGNORECASE,
)


def extract_pdf_text_with_pages(pdf_path: str) -> str:
    """Extract text from PDF, inserting [PAGE X] markers for each page."""
    reader = PdfReader(pdf_path)
    full_text = ""

    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = _HEADER_PATTERN.sub("", text)
        full_text += f"\n[PAGE {i}]\n{text}\n"

    return full_text.strip()


def get_pdf_page_count(pdf_path: str) -> int:
    reader = PdfReader(pdf_path)
    return len(reader.pages)


def list_unit_pdfs(directory: str) -> list[str]:
    """Return sorted list of PDF paths found in directory (recursively)."""
    pdfs = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(".pdf"):
                pdfs.append(os.path.join(root, f))
    return sorted(pdfs)


def infer_unit_number(pdf_path: str) -> int:
    """Try to extract unit number from filename or path."""
    import re
    name = os.path.basename(pdf_path).lower()
    match = re.search(r"unit\s*(\d+)", name)
    if match:
        return int(match.group(1))
    # try parent folder
    folder = os.path.basename(os.path.dirname(pdf_path)).lower()
    match = re.search(r"unit\s*(\d+)", folder)
    if match:
        return int(match.group(1))
    return 1
