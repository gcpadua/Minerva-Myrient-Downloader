# Minerva Myrient Downloader

A command-line tool built in Python to easily search, select, and download specific files from the Minerva Myrient archives via torrents. 

Torrent GUIs can become slow and cumbersome when dealing with dumps containing tens of thousands of files. This tool solves that by parsing pre-generated markdown lists of file IDs, allowing you to search for specific games, select them, and download only what you need using `aria2c`.

## Prerequisites

- **Python 3.x**
- **PyInstaller** (if you wish to build the standalone executable)
```bash
  pip install pyinstaller
```
- **Aria2**
 - Linux: Must be installed on the system (e.g., `sudo apt install aria2`).
 - Windows: The `aria2c.exe` binary must be placed inside the `aria2` folder before compilation. See https://aria2.github.io/
- **Torrent files** download the torrent from Minerva for the desired dump (https://cdn.minerva-archive.org/torrents/) and place them on the `torrent` folder

# Compilation Instructions
You can build a standalone executable that bundles the necessary torrent and markdown files.

## Windows
On Windows, the `aria2c.exe` binary is bundled inside the executable. Run the following command in the project root:
```powershell
  pyinstaller --noconfirm --onefile --add-data "aria2;aria2" --add-data "markdown;markdown" --add-data "torrent;torrent" main.py
```

## Linux
On Linux, the tool relies on the system's native aria2c installation, so you do not need to bundle the binary. Note the use of a colon (:) instead of a semicolon (;) for the --add-data flags. Run:
```bash
  pyinstaller --noconfirm --onefile --add-data "markdown:markdown" --add-data "torrent:torrent" main.py
```
After compilation, the standalone binary will be located in the dist folder.

# Execution Instructions
## Windows
Simply double-click the generated main.exe file inside the dist folder, or run it via the command prompt:
```powershell
  cd dist
  main.exe
```
## Linux
Navigate to the dist folder and execute the binary:
```bash
  cd dist
  ./main
```
# Usage
1. Select the system/archive you want to browse from the presented list.

2. Choose to either list all games or search for specific terms.

3. Enter the IDs of the files you want to download (e.g., 1,3,5-10).

4. Confirm your selection. The tool will automatically call aria2c and download the selected pieces.

5. Files will be saved in a download folder in the same directory where the executable was run.

# Acknowledgements
Special thanks to Caprico1 and the Caprico1/Minerva-archive-ids repository. Their work in scraping and mapping the file IDs for each Minerva torrent dump made this project possible.
