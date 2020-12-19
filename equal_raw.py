"""Equal Photos - used to find and isolate raw files according to jpg or vice versa.

Version: 2020.12.1

Author:     Markus Kary
Contact:    devel@maky.at

License:    GPLv3 or higher
"""
import os
import sys
import shutil
from time import sleep

# Set your default preferences here:
DEFAULT_PRIMARY_EXT = "jpg"
DEFAULT_SECONDARY_EXT = "NEF"
ISOLATION = "Isolation"
DEFAULT_PRIMARY_DIR = "/Users/markus/ZZ_Ablage_ungesichert/FotoTest/toast"
# Extensions to search for:
JPG_EXTENTIONS = ["jpg", "JPG", "jpeg", "JPEG"]
RAW_EXTENSIONS = ["nef", "NEF", "RW2", "rw2", "DNG", "dng"]

DEBUG = False


def main() -> None:
    """Run main program."""
    primary_dir, secondary_dir = get_dir_information()
    if not create_iso_dir(primary_dir):
        sys.exit()
    print(f"Isolation directory created at... \n{primary_dir}/{ISOLATION}")

    primary_files = create_primary_file_list(primary_dir, JPG_EXTENTIONS)
    secondary_files = create_secondary_file_list(
        secondary_dir, primary_files, RAW_EXTENSIONS)
    moved_counter, error_counter = move_files_to_isolation(
        primary_dir, secondary_dir, secondary_files)

    if moved_counter > 0:
        print(f"Done!\nMoved {moved_counter} files to {ISOLATION}. "
              f"Skipped {error_counter} Files.")
    else:
        print(f"No files to move. {error_counter} files skipped.")

    deletion(moved_counter, primary_dir)


def get_dir_information() -> tuple:
    """Collect information on directorys to deal with."""
    primary_dir = input(
        "Write or drop JPG directory: _") or DEFAULT_PRIMARY_DIR
    secondary_format = input(
        f"What is the RAW folder called: (Default {DEFAULT_PRIMARY_EXT})? _") or DEFAULT_PRIMARY_EXT
    secondary_dir = f"{primary_dir}/{secondary_format}"
    secondary_dir = input(
        f"Is this the correct RAW directory: '{secondary_dir}'") or secondary_dir
    return (primary_dir, secondary_dir)


def create_iso_dir(dirpath) -> bool:
    """Create directory for isolated files.
    Skipped if directory exists
    """
    try:
        os.mkdir(f"{dirpath}/{ISOLATION}")
        return True
    except FileExistsError:
        return True
    except Exception as error:
        print(f"Error creating isolation directory {error}")
        return False


def create_primary_file_list(file_dir, extensions) -> list:
    """Return the filenames to keep in secondary_dir without extension."""
    filenames = []
    for file in os.listdir(file_dir):
        for ext in extensions:
            if file.find(ext) > 0:
                filename = file.split(f".{ext}")[0]
                filenames.append(filename)
    return filenames


def create_secondary_file_list(secondary_dir, primary_files, extensions) -> list:
    """Returns the list of files to move."""
    print("Moving files...")
    files_to_move = []
    # Create list of all possible combination to find.
    files_to_search = []
    for file in primary_files:
        for ext in extensions:
            files_to_search.append(f"{file}.{ext}")
    # Search for files to move.
    for file in os.listdir(secondary_dir):
        if file not in files_to_search:
            files_to_move.append(file)
    return files_to_move


def move_files_to_isolation(primary_dir, secondary_dir, secondary_files) -> tuple:
    """Move the files."""
    iso_dir = f"{primary_dir}/{ISOLATION}"
    moved_counter = 0
    error_counter = 0
    for file in secondary_files:
        if DEBUG:
            print(f"{primary_dir}/{file}")
        try:
            # print(f"{secondary_dir}/{file}", f"{iso_dir}")
            shutil.move(f"{secondary_dir}/{file}", f"{iso_dir}/")
            moved_counter += 1
        except FileNotFoundError as error:
            pass
        except OSError as error:
            error_counter += 1
        except Exception as error:
            print(error)
            sys.exit()
    return (moved_counter, error_counter)


def deletion(moved_counter, primary_dir) -> None:
    """Delete isolated files and directory."""
    counter = 10
    if moved_counter > 0:
        delete = input("\n\n"
                       f"Would you like to remove the {moved_counter} "
                       f"files in {ISOLATION}?\n"
                       "WARNING: This cannot be undone!!!\n\n"
                       "Type 'yes' to move on.\n"
                       "Every other input to abort. (Default no)_") or "no"

        if delete == "yes":
            try:
                while counter > 0:
                    print(f"Waiting {counter} seconds. Ctrl-c to abort.")
                    counter -= 1
                    sleep(1)
                shutil.rmtree(f"{primary_dir}/{ISOLATION}")
            except KeyboardInterrupt:
                print("\n\nCtrl-C detected. Deletion aborted...\n")
                sys.exit()
        else:
            sys.exit()


if __name__ == "__main__":
    main()
