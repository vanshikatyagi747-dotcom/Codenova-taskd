import os
import shutil
from pathlib import Path

# --- Configuration Mapping ---
# Dictionary defining target folder structures and their associated file extensions
EXTENSION_MAPPING = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".ppt", ".csv", ".md"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Video": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programs_Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".sh"]
}

def organize_folder(target_directory):
    """Iterates over a target directory and organizes unstructured files into sorted sub-folders."""
    target_path = Path(target_directory)

    # 1. Validation check ensuring the requested directory path exists safely
    if not target_path.exists():
        print(f"❌ Error: The directory path '{target_directory}' does not exist.")
        return
    if not target_path.is_dir():
        print(f"❌ Error: '{target_directory}' is a file path, not a valid directory container.")
        return

    print(f"⚡ Scanning directory: {target_path.resolve()}...")
    moved_count = 0

    # 2. Iterate through every single item directly inside the targeted path
    for item in target_path.iterdir():
        # Bypass sorting operations on folder directories inside the root target path
        if item.is_dir():
            continue

        # Extract file extension string suffix in lower case formatting
        file_extension = item.suffix.lower()
        
        # Track whether the file matches one of our defined categories
        category_found = False

        for folder_name, extensions in EXTENSION_MAPPING.items():
            if file_extension in extensions:
                # Construct destination sub-folder path dynamically
                destination_folder = target_path / folder_name
                
                # Make the category folder safely if it doesn't already exist
                destination_folder.mkdir(exist_ok=True)
                
                # Relocate item into organized path layout
                destination_path = destination_folder / item.name
                
                try:
                    shutil.move(str(item), str(destination_path))
                    print(f"📁 Moved: {item.name} ➡️  {folder_name}/")
                    moved_count += 1
                except Exception as e:
                    print(f"❌ Could not move file {item.name}. Reason: {e}")
                
                category_found = True
                break

        # Optional: Handle miscellaneous file items that do not fit standard maps
        if not category_found and file_extension:
            other_folder = target_path / "Others"
            other_folder.mkdir(exist_ok=True)
            try:
                shutil.move(str(item), str(other_folder / item.name))
                print(f"📁 Moved: {item.name} ➡️  Others/")
                moved_count += 1
            except Exception as e:
                print(f"❌ Could not move file {item.name}. Reason: {e}")

    print(f"\n✅ Execution Finished! Successfully organized {moved_count} file items.")

if __name__ == "__main__":
    # --- Input Processing Choice ---
    # You can type an absolute file path pattern here (e.g., "C:/Users/Name/Downloads")
    # Leaving it empty as dot notation "." evaluates actions on the script's exact working location.
    target_dir = input("Enter path to organize (Press Enter for current directory '.'): ").strip()
    
    if not target_dir:
        target_dir = "."
        
    organize_folder(target_dir)
