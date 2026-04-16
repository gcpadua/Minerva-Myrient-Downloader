import os

DEST_DIR = ".torrent"

def rename_torrents():
    
    if not os.path.isdir(DEST_DIR):
        print(f"Folder {DEST_DIR} not found.")
        return

    for filename in os.listdir(DEST_DIR):
        old_path = os.path.join(DEST_DIR, filename)
        
        if os.path.isfile(old_path):
            new_filename = filename.replace(" ", "_")
            new_path = os.path.join(DEST_DIR, new_filename)
            if new_path != old_path:
                print(f"Renaming: {filename} -> {new_filename}")
                os.rename(old_path, new_path)

if __name__ == "__main__":
    rename_torrents()
