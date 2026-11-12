
import json
from pathlib import Path

from app.models import Record

RAW_DIR = Path("data/raw")
OUTPUT_FILE = Path("data/records.json")

RECORD_DETAILS = {
    "password_storage.md": {
        "vulnerability": "Weak password storage can expose user credentials.",
        "recommended_control": "Use Argon2id or another approved password hashing algorithm with unique salts.",
        "exact_parameter": "Password hashing algorithm, work factor and unique salt",
        "owasp_top10_category": "A04:2025 Cryptographic Failures"
    },

    "authentication.md": {
        "vulnerability": "Weak authentication can allow attackers to access user accounts.",
        "recommended_control": "Use secure authentication, multifactor authentication and appropriate login protections.",
        "exact_parameter": "Authentication methods and login attempt limits",
        "owasp_top10_category": "A07:2025 Authentication Failures"
    },

    "sql_injection.md": {
        "vulnerability": "Untrusted input can change the meaning of database queries.",
        "recommended_control": "Use parameterized queries or prepared statements.",
        "exact_parameter": "SQL query parameters and prepared statements",
        "owasp_top10_category": "A05:2025 Injection"
    }
}

SOURCE_URLS = {
    "password_storage.md": "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Password_Storage_Cheat_Sheet.md",

    "authentication.md": "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Authentication_Cheat_Sheet.md",

    "sql_injection.md": "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.md"
}


def clean_record(file_path):
    try:
        content = file_path.read_text(encoding="utf-8")

        if not content.strip():
            raise ValueError("Empty document")

        title = ""

        for line in content.splitlines():
            if line.startswith("# "):
                title = line.replace("#", "", 1).strip()
                break

        if not title:
            raise ValueError("Document title not found")

        details = RECORD_DETAILS.get(file_path.name)

        if details is None:
            raise ValueError("No security details available")

        source_url = SOURCE_URLS[file_path.name]

        record = Record(
            cheat_sheet=title,
            vulnerability=details["vulnerability"],
            recommended_control=details["recommended_control"],
            exact_parameter=details["exact_parameter"],
            owasp_top10_category=details["owasp_top10_category"],
            source_url=source_url
        )

        return record.to_dict()

    except (OSError, ValueError, KeyError, AttributeError) as error:
        print(f"Skipping bad row {file_path.name}: {error}")
        return None


def ingest_data():
    try:
        records = []

        for file_path in RAW_DIR.glob("*.md"):
            record = clean_record(file_path)

            if record is not None:
                records.append(record)

        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        OUTPUT_FILE.write_text(
            json.dumps(records, indent=4),
            encoding="utf-8"
        )

        print("Ingestion completed!")
        print("Records saved:", len(records))
        print("Output file:", OUTPUT_FILE)

    except OSError as error:
        print("Ingestion file error:", error)


if __name__ == "__main__":
    ingest_data()
