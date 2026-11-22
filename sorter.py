from pathlib import Path
import shutil

# Which file types go in which folder
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".pptx", ".xlsx", ".csv"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav", ".m4a"],
    "Archives": [".zip", ".rar", ".7z"],
}


def get_category(file):
    extension = file.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Other"


def unique_path(path):
    # If a file with the same name exists, add (1), (2), etc. instead of overwriting
    counter = 1
    new_path = path
    while new_path.exists():
        new_path = path.with_name(f"{path.stem} ({counter}){path.suffix}")
        counter += 1
    return new_path


def main():
    folder = Path(input("Folder to sort: ").strip().strip('"'))

    if not folder.is_dir():
        print("That folder doesn't exist.")
        return

    files = [f for f in folder.iterdir() if f.is_file()]
    if not files:
        print("No files to sort.")
        return

    # Preview first, so nothing moves without your approval
    plan = [(file, get_category(file)) for file in files]
    print("\nHere is what will happen:")
    for file, category in plan:
        print(f"  {file.name}  ->  {category}/")

    answer = input("\nMove these files? (y/n): ").strip().lower()
    if answer != "y":
        print("Cancelled. Nothing was moved.")
        return

    for file, category in plan:
        destination_folder = folder / category
        destination_folder.mkdir(exist_ok=True)
        shutil.move(str(file), str(unique_path(destination_folder / file.name)))

    print("Done!")


main()