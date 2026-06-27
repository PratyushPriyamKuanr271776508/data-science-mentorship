import os
import gdown
from urllib.parse import urlparse, parse_qs


def extract_google_drive_id(link: str) -> str:
    """Extract the Google Drive file or folder ID from a share link."""
    parsed = urlparse(link)
    if parsed.netloc in {"drive.google.com", "www.drive.google.com"}:
        if "/file/d/" in parsed.path:
            return parsed.path.split("/file/d/")[1].split("/", 1)[0]
        if "/folders/" in parsed.path:
            return parsed.path.split("/folders/")[1].split("/", 1)[0]
        if parsed.query:
            return parse_qs(parsed.query).get("id", [None])[0]
    return None


def download_item(link: str, destination: str) -> str:
    """Download a Google Drive file or folder to the destination path."""
    os.makedirs(destination, exist_ok=True)
    item_id = extract_google_drive_id(link)
    if not item_id:
        raise ValueError("Could not parse the Google Drive link.")

    if "/folders/" in link or "drive.google.com/drive/folders/" in link:
        output = gdown.download_folder(link, output=destination, quiet=False, use_cookies=False)
    else:
        output = gdown.download(link, output=os.path.join(destination, "downloaded_file"), quiet=False, fuzzy=True)
    return output if isinstance(output, str) else destination


if __name__ == "__main__":
    google_link = input("Enter the Google Drive share link: ").strip()
    destination = input("Enter the destination folder path in this workspace: ").strip()
    destination = os.path.abspath(destination)

    downloaded = download_item(google_link, destination)
    print(f"Download completed. Files saved to: {destination}")
