
import requests
from pathlib import Path


RAW_DIR = Path("data/raw")

DOCUMENTS = {
    "password_storage.md":
        "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Password_Storage_Cheat_Sheet.md",

    "authentication.md":
        "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Authentication_Cheat_Sheet.md",

    "sql_injection.md":
        "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.md"
}


def fetch_documents():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for filename, url in DOCUMENTS.items():
        try:
            response = requests.get(url, timeout=15)

            response.raise_for_status()

            file_path = RAW_DIR / filename
            file_path.write_text(response.text, encoding="utf-8")

            print(f"Downloaded successfully: {filename}")

        except requests.exceptions.Timeout:
            print(f"Timeout error while downloading: {filename}")

        except requests.exceptions.HTTPError as error:
            print(f"HTTP error for {filename}: {error}")

        except requests.exceptions.RequestException as error:
            print(f"Download error for {filename}: {error}")

        except OSError as error:
            print(f"File saving error for {filename}: {error}")


if __name__ == "__main__":
    fetch_documents()
