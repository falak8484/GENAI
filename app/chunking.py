
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_FILE = BASE_DIR / "data" / "chunks.json"

MAX_CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def split_text(text, max_size=MAX_CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split long text into smaller chunks with overlapping content."""

    text = text.strip()

    if not text:
        return []

    if max_size <= 0:
        raise ValueError("max_size must be greater than 0")

    if overlap < 0 or overlap >= max_size:
        raise ValueError("overlap must be >= 0 and smaller than max_size")

    if len(text) <= max_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + max_size, len(text))

        if end < len(text):
            boundary = text.rfind("\n", start, end)

            if boundary < start + max_size // 2:
                boundary = text.rfind(" ", start, end)

            if boundary > start:
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(end - overlap, start + 1)

    return chunks


def extract_sections(file_path):
    """Extract Markdown sections and their titles."""

    lines = file_path.read_text(encoding="utf-8").splitlines()

    document_title = file_path.stem.replace("_", " ").title()

    for line in lines:
        if line.startswith("# "):
            document_title = line[2:].strip()
            break

    sections = []
    current_title = document_title
    current_lines = []

    for line in lines:
        heading = re.match(r"^#{2,6}\s+(.+)", line)

        if heading:
            previous_content = "\n".join(current_lines).strip()

            if previous_content:
                sections.append((current_title, previous_content))

            current_title = heading.group(1).strip()
            current_lines = []

        elif line.startswith("# "):
            continue

        else:
            current_lines.append(line)

    final_content = "\n".join(current_lines).strip()

    if final_content:
        sections.append((current_title, final_content))

    return sections


def chunk_documents(
    max_size=MAX_CHUNK_SIZE,
    overlap=CHUNK_OVERLAP
):
    """Create chunks from all OWASP Markdown documents."""

    all_chunks = []

    for file_path in sorted(RAW_DIR.glob("*.md")):
        sections = extract_sections(file_path)

        for title, content in sections:
            text_chunks = split_text(
                content,
                max_size=max_size,
                overlap=overlap
            )

            for chunk_text in text_chunks:
                chunk_id = f"{file_path.stem}-{len(all_chunks) + 1:04d}"

                all_chunks.append({
                    "id": chunk_id,
                    "text": f"{title}\n{chunk_text}",
                    "source": file_path.name,
                    "page": None,
                    "title": title
                })

    return all_chunks


def save_chunks(chunks, output_file):
    """Save generated chunks to a JSON file."""

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    output_file.write_text(
        json.dumps(chunks, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("Total chunks:", len(chunks))
    print("Saved to:", output_file)


if __name__ == "__main__":

    chunks = chunk_documents()

    save_chunks(chunks, OUTPUT_FILE)

    print("\nChunking completed!")

    if chunks:
        print("\nFirst chunk:")
        print("Source:", chunks[0]["source"])
        print("Page:", chunks[0]["page"])
        print("Title:", chunks[0]["title"])
        print("Text:", chunks[0]["text"][:300])
