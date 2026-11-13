
import json
from pathlib import Path

from app.models import Record

RAW_DIR = Path("data/raw")
OUTPUT_FILE = Path("data/records.json")

SOURCE_URLS = {
    "authentication.md": "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Authentication_Cheat_Sheet.md",
    "password_storage.md": "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Password_Storage_Cheat_Sheet.md",
    "sql_injection.md": "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.md"
}

RULES = {
    "authentication.md": {
        "Implement Proper Password Strength Controls": (
            "Weak or easily guessed passwords can allow attackers to access user accounts.",
            "Enforce appropriate password length and strength controls, and prevent commonly used passwords.",
            "Password length, password blocklist and password policy",
            "A07:2025 Authentication Failures"
        ),
        "Store Passwords in a Secure Fashion": (
            "Insecure password storage can expose user credentials if the database is compromised.",
            "Store passwords using a secure adaptive hashing algorithm such as Argon2id, scrypt or PBKDF2.",
            "Password hashing algorithm, salt and work factor",
            "A07:2025 Authentication Failures"
        ),
        "Compare Password Hashes Using Safe Functions": (
            "Unsafe password-hash comparison can expose information through timing differences.",
            "Use a secure password comparison function provided by the programming language or framework.",
            "Constant-time password hash comparison function",
            "A07:2025 Authentication Failures"
        ),
        "Protect Against Automated Attacks": (
            "Automated attacks such as brute force and credential stuffing can compromise user accounts.",
            "Apply login protections such as rate limiting, monitoring and multifactor authentication.",
            "Login attempt limits, rate limiting and MFA",
            "A07:2025 Authentication Failures"
        ),
        "Require Re-authentication for Sensitive Features": (
            "An attacker with access to an active session may attempt sensitive account changes.",
            "Require users to confirm their current credentials before sensitive account changes or transactions.",
            "Re-authentication for password, email and sensitive transaction changes",
            "A07:2025 Authentication Failures"
        )
    },

    "password_storage.md": {
        "Salting": (
            "Without unique salts, identical passwords can produce matching hashes and make bulk cracking easier.",
            "Generate a unique random salt for each password and include it in the password-hashing process.",
            "Unique random salt per password",
            "A04:2025 Cryptographic Failures"
        ),
        "Peppering": (
            "An attacker who obtains password hashes from a database may attempt to crack them.",
            "Consider using a pepper as an additional secret stored separately from the password database.",
            "Pepper secret and its secure storage location",
            "A04:2025 Cryptographic Failures"
        ),
        "Using Work Factors": (
            "Low password-hashing work factors can make password cracking faster.",
            "Configure an appropriate work factor to make password hashing computationally expensive.",
            "Password hashing work factor or cost setting",
            "A04:2025 Cryptographic Failures"
        ),
        "Argon2id": (
            "Using an unsuitable password-hashing algorithm can weaken stored password protection.",
            "Prefer Argon2id for password storage and configure its parameters according to security and performance needs.",
            "Argon2id memory, time and parallelism parameters",
            "A04:2025 Cryptographic Failures"
        ),
        "bcrypt": (
            "Using outdated or weak password-hashing settings can make password hashes easier to crack.",
            "Use bcrypt mainly for legacy systems when Argon2 or scrypt is unavailable, with a work factor of at least 10.",
            "bcrypt work factor, minimum 10",
            "A04:2025 Cryptographic Failures"
        )
    },

    "sql_injection.md": {
        "Parameterized Queries": (
            "Concatenating untrusted input into SQL statements can allow attackers to change query behavior.",
            "Use parameterized queries or prepared statements to keep SQL structure separate from user-supplied values.",
            "SQL parameter binding and prepared statements",
            "A05:2025 Injection"
        ),
        "Allow-List Input Validation": (
            "Untrusted input used for SQL identifiers or query structure can introduce injection risks.",
            "Use an allow-list of permitted table names, column names or sort directions when these choices must be dynamic.",
            "Allow-listed SQL identifiers and permitted query options",
            "A05:2025 Injection"
        ),
        "Least Privilege": (
            "Excessive database permissions can increase the damage caused by a successful SQL injection attack.",
            "Give application database accounts only the permissions required for their tasks.",
            "Database account permissions and privileges",
            "A05:2025 Injection"
        ),
        "Manually escaping (STRONGLY DISCOURAGED)": (
            "Manual escaping of untrusted SQL input is error-prone and can fail to prevent injection.",
            "Avoid manually escaping SQL values. Use parameterized queries instead.",
            "SQL parameter binding instead of manual escaping",
            "A05:2025 Injection"
        ),
        "Input Validation": (
            "Invalid or unexpected input can create application security risks, including SQL injection when used unsafely.",
            "Validate input according to expected type, length and format, while continuing to use parameter binding.",
            "Input type, length and format validation",
            "A05:2025 Injection"
        )
    }
}


def clean_record(file_path, heading, details):
    try:
        content = file_path.read_text(encoding="utf-8")
        lines = content.splitlines()

        title = next(
            (line[2:].strip() for line in lines if line.startswith("# ")),
            None
        )

        if not title:
            raise ValueError("Document title not found")

        if not any(line.strip() == f"### {heading}" for line in lines):
            raise ValueError(f"Rule heading not found: {heading}")

        vulnerability, control, parameter, category = details

        record = Record(
            cheat_sheet=title,
            vulnerability=vulnerability,
            recommended_control=control,
            exact_parameter=parameter,
            owasp_top10_category=category,
            source_url=SOURCE_URLS[file_path.name]
        )

        return record.to_dict()

    except (OSError, ValueError, KeyError, AttributeError) as error:
        print(f"Skipping {heading}: {error}")
        return None


def ingest_data():
    records = []

    for filename, rules in RULES.items():
        file_path = RAW_DIR / filename

        if not file_path.exists():
            print(f"Missing source file: {filename}")
            continue

        for heading, details in rules.items():
            record = clean_record(file_path, heading, details)

            if record is not None:
                records.append(record)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(records, indent=4),
        encoding="utf-8"
    )

    print("\nIngestion completed!")
    print("Records saved:", len(records))
    print("Output file:", OUTPUT_FILE)

    for record in records:
        print("-", record["cheat_sheet"], "|", record["exact_parameter"])


if __name__ == "__main__":
    ingest_data()
