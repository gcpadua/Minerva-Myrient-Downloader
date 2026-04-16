import os
import sys
import shutil
import platform
import subprocess

def parse_md_table(file_path: str) -> list:
	"""
	Reads a .md file containing a table and returns a list of dictionaries.
	"""
	parsed_data = []
		
	# Verifies if the file exists
	if not os.path.exists(file_path):
		raise FileNotFoundError(f"File: {file_path} not found.")

	with open(file_path, 'r', encoding='utf-8') as file:
		for line in file:
			line = line.strip()
			
			if line.startswith('|') and line.endswith('|'):
				parts = line.split('|')
				
				if len(parts) >= 3:
					id_str = parts[1].strip()
					name_str = parts[2].strip()
					
					try:
						item_id = int(id_str)
						parsed_data.append({
							'id': item_id,
							'name': name_str.split('/')[-1].replace('.zip', '').strip()
						})
					except ValueError:
						continue
						
	return parsed_data

def parse_selection(selection: str) -> list:
	"""
	Parses a user selection string and returns a list of integers.
	"""
	if not selection or 'q' in selection:
		return []
	ids = []
	for part in selection.split(','):
		part = part.strip()
		if '-' in part:
			start, end = part.split('-')
			try:
				start_id = int(start)
				end_id = int(end)
				ids.extend(range(start_id, end_id + 1))
			except ValueError:
				continue
		else:
			try:
				ids.append(int(part))
			except ValueError:
				continue
	return ids

def get_resource_path(relative_path: str) -> str:
    """
    Returns the absolute path to the resource, whether in development mode
    or running as a compiled binary by PyInstaller.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
	# Relevant folders
	if platform.system() == "Windows":
		aria2_folder = get_resource_path("aria2")
	torrent_folder = get_resource_path("torrent")
	markdown_folder = get_resource_path("markdown")

	#List all files in the markdown folder
	markdown_files = [ f for f in os.listdir(markdown_folder) if f.endswith('.md') ]
	md_with_matching_torrent = [ f for f in markdown_files if f.replace('-ids.md', '') in os.listdir(torrent_folder) ]

	print("Select the system you want to browse:")
	for i, file in enumerate(md_with_matching_torrent):
		print(f"{i + 1}. {file.replace('Minerva_Myrient_-_', '').replace('.torrent-ids.md', '').replace('_', ' ').strip()}")
		
	choice = int(input("Enter your choice: ")) - 1
	selected_file = md_with_matching_torrent[choice]

	chosen_system = os.path.join(markdown_folder, selected_file)
	games = parse_md_table(chosen_system)
	ids = []
	selection = ''
	while selection not in ['l', 's']:
		selection = input("Do you want to (l)ist all games or (s)earch for a specific game? (l/s): ").lower()
	if selection == 'l':
		for game in games:
			print(f"{game['id']}: {game['name']}")
			if game['id'] % 25 == 0:
				selection = input("Type the ids you want to download (e.g., 1,3,5-10) or 'q' to quit: ")
				ids.extend(parse_selection(selection))
				if selection.lower() == 'q':
					break
	elif selection == 's':
		while selection != 'n':
			search_results = []
			search_terms = input("Enter the terms you want to search for separated by spaces: ").lower()
			for game in games:
				if all(term in game['name'].lower() for term in search_terms.split()):
					print(f"{game['id']}: {game['name']}")
					search_results.append(game)
			if search_results:
				selection = input("Type the ids you want to download (e.g., 1,3,5-10) or 'a' to select all: ")
				if selection.lower() == 'a':
					ids.extend([game['id'] for game in search_results])
				else:
					ids.extend(parse_selection(selection))
			selection = input("Do you want to search for another game? (y/n): ").lower()
		
	print("Game selection completed.\nThe following games will be downloaded:")
	for game in games:
		if game['id'] in ids:
			print(f"{game['id']}: {game['name']}")
	selection = input("Do you want to proceed with the download? (y/n): ").lower()
	if selection == 'n':
		print("Download cancelled.")
	elif selection == 'y':
		print("Starting download...")
		ids_str = ','.join(str(id) for id in ids)
		# Execute aria2c --select-file=<id> --seed-time=0 <torrent_file> -d <directory_to_save_file_to>
		torrent_file = os.path.join(torrent_folder, selected_file.replace('-ids.md', ''))
		if platform.system() == "Windows":
			command = f"aria2c --select-file={ids_str} --seed-time=0 {torrent_file} -d download --bt-remove-unselected-file=true"
		else:
			if shutil.which("aria2c") is None:
				print("Error: 'aria2c' not found in the system.")
				print("Please install it using your package manager (e.g., sudo apt install aria2).")
				sys.exit(1)
			command = f"aria2c --select-file={ids_str} --seed-time=0 {torrent_file} -d download --bt-remove-unselected-file=true"
		subprocess.run(command, shell=True)
		input("Download completed.\nFiles saved to the 'download' folder.\nPress Enter to exit.")
