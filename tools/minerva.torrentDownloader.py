from bs4 import BeautifulSoup
import requests
import time
import os

BASE_URL = "https://cdn.minerva-archive.org/torrents/"
DEST_DIR = "torrent"

def download_torrents():
    os.makedirs(DEST_DIR, exist_ok=True)

    resp = requests.get(BASE_URL)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].endswith(".torrent")]

    for link in links:
        url = BASE_URL + link
        filename = os.path.join(DEST_DIR, os.path.basename(link)).replace("%20", "_")

        if not os.path.exists(filename):
            print(f"Downloading {filename}...")
            r = requests.get(url)
            r.raise_for_status()
            with open(filename, "wb") as f:
                f.write(r.content)
        else:
            print(f"{filename} already exists, skipping .")

        time.sleep(3) 

if __name__ == "__main__":
    download_torrents()
