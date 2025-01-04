import time
import webbrowser
from datetime import timedelta
from pathlib import Path

import mw2gc

URL_GARMIN_IMPORT = "https://connect.garmin.com/modern/import-data"

URL_MW_ACTIVITIES = "https://event.mywhoosh.com/user/activities"

THRESHOLD_FIT_FILES = timedelta(hours=6)


def get_browser():
    return webbrowser.Mozilla(r"C:\Program Files\Firefox Nightly\firefox.exe")


def get_fit_files(path: Path, since: timedelta):
    threshold = time.time() - since.total_seconds()
    fit_files = [file for file in path.glob("*.fit") if file.stat().st_ctime > threshold]
    return fit_files


def main():
    # Set up constants
    downloads_dir = Path.home().joinpath("Downloads")

    browser = get_browser()

    # Print message about downloading data
    print(f"Please download all data from {URL_MW_ACTIVITIES} > Activities tab")
    browser.open_new_tab(URL_MW_ACTIVITIES)

    # Wait for user to finish downloading
    activity_name = input("Enter activity name copied from MyWhoosh:\n").strip()

    fit_files = get_fit_files(downloads_dir, THRESHOLD_FIT_FILES)

    # Process each .dms file in Downloads
    for file in fit_files:
        print(f"Now processing file {file}")
        # Directly call the convert() function from mw2gc.py
        mw2gc.convert(str(file), debug=True)
        file.unlink()  # Remove the file after processing

    # Copy the absolute paths of the .fit files to clipboard
    fixed_files = get_fit_files(downloads_dir, since=THRESHOLD_FIT_FILES)

    # Print message for the user
    print(f"Files ready for upload on {URL_GARMIN_IMPORT}:\n{''.join([str(file) for file in fixed_files])}")
    if activity_name:
        print(f"Your activity name is:\n{activity_name}")
    browser.open_new_tab(URL_GARMIN_IMPORT)

    # Wait for user to finish uploading
    input("Press enter once done to delete all fit files...")

    # Delete the .fit files after upload
    for fit_file in fixed_files:
        fit_file.unlink()


if __name__ == "__main__":
    main()
