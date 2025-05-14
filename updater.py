import os
import requests
import zipfile
import time
import shutil

from langs import langs

# INSTALL_DIR is the name of the current directory, which is also where the new version gets installed
INSTALL_DIR = os.path.dirname(os.path.abspath(__file__))

LOCAL_VERSION_PATH = os.path.join(INSTALL_DIR, "version.txt")
ONLINE_VERSION_PATH = "https://api.github.com/repos/MabelTheCat/InteligenteChemistryQuizzes/releases/latest"

VERSION_SPLIT_CHAR = "."

def compare_versions(v1: str, v2: str):
    """Compares two versions, checking from left to right.
    \nReturns `1` if `v1 > v2`, returns `0` if `v1 == v2`, returns `-1` if `v1 < v2`"""
    v1_numbers = []
    for chunk in v1.split(VERSION_SPLIT_CHAR):
        v1_numbers.append(int(chunk))

    v2_numbers = []
    for chunk in v2.split(VERSION_SPLIT_CHAR):
        v2_numbers.append(int(chunk))

    # Compare v1 and v2
    for i in range(len(v1_numbers)):
        if v1_numbers[i] > v2_numbers[i]:
            return 1
        
        elif v1_numbers[i] < v2_numbers[i]:
            return -1

    return 0

def check_for_update(lang: str = "en") -> bool | None:
    global response

    try:
        response = requests.get(ONLINE_VERSION_PATH)
    except Exception as error:
        print(langs.get_updater_item("conn_failed", lang).format(error))
        return

    if response.status_code != 200:
        print(langs.get_updater_item("version_get_fail", lang).format(response.status_code))
        return

    online_version = response.json()["tag_name"][1:6]
    
    if os.path.exists(LOCAL_VERSION_PATH):
        with open(LOCAL_VERSION_PATH, "r", encoding="utf-8") as fo:
            local_version = fo.read().strip()
    
    else:
        print(langs.get_updater_item("local_version_not_found", lang))
        if input(langs.get_updater_item("update_anyhow", lang)).upper() in langs.get_ui_text("confirm", lang):

            # Set local version to lowest possible to force an update
            local_version = "0.0.-1"

        else:
            return False

    if compare_versions(online_version, local_version) == 1:
        return True
    
    else:
        return False

def run(lang: str = "en"):

    print(langs.get_updater_item("update_check", lang))
    if (update_available := check_for_update(lang)):
        print(langs.get_updater_item("update_found", lang))

        if input(langs.get_updater_item("ask_to_update", lang)).upper() not in langs.get_ui_text("confirm", lang):
            return

        if input(langs.get_updater_item("request_update_type", lang)).upper() == "S":
            # Get the link to the zipped source code folder
            for asset in response.json()["assets"]:
                if "SRC" in asset["name"]:
                    download_url = asset["browser_download_url"]

        else:
            # Get the link to the zipped executable folder
            for asset in response.json()["assets"]:
                if "EXE" in asset["name"]:
                    download_url = asset["browser_download_url"]

        print(langs.get_updater_item("updating", lang))
        
        print(f"{'X'*0}{'-'*8} (0%)   ", end="", flush=True)
        OLD_DIR = INSTALL_DIR + "_old"

        # Create old directory
        i = 0
        while os.path.exists(OLD_DIR):
            OLD_DIR = OLD_DIR[:len(INSTALL_DIR + "_old")] + str(i)
            i += 1

        print(f"\r{'X'*1}{'-'*7} (12.5%)", end="", flush=True)
        
        ZIP_PATH = os.path.join(OLD_DIR, ".temp_install.zip")

        # Get the file and download it
        try:
            code = requests.get(download_url)
        except Exception as error:
            print(langs.get_updater_item("conn_failed", lang).format(error))
            return
        
        print(f"\r{'X'*2}{'-'*6} (25%)  ", end="", flush=True)

        shutil.move(INSTALL_DIR, OLD_DIR)
        print(f"\r{'X'*3}{'-'*5} (37.5%)", end="", flush=True)

        with open(ZIP_PATH, "wb") as f:
            f.write(code.content)

        print(f"\r{'X'*4}{'-'*4} (50%)  ", end="", flush=True)

        print(f"\r{'X'*5}{'-'*3} (62.5%)", end="", flush=True)
        with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
            zip_ref.extractall(os.path.dirname(INSTALL_DIR))
            ZIP_NAME = list(zip_ref.NameToInfo.keys())[0].split("/")[0]

        print(f"\r{'X'*6}{'-'*2} (75%)  ", end="", flush=True)
        os.remove(ZIP_PATH)

        print(f"\r{'X'*7}{'-'*1} (87.5%)", end="", flush=True)

        shutil.move(os.path.join(os.path.dirname(INSTALL_DIR), ZIP_NAME), INSTALL_DIR)
        print(f"\r{'X'*8}{'-'*0} (100%) ", end="", flush=True)
        print(langs.get_updater_item("update_complete", lang))
        return

    elif update_available == False:
        print(langs.get_updater_item("already_up_to_date", lang))
        return
    
    else:
        return

if __name__ == "__main__":
    run()
    print(langs.get_updater_item("window_close", "en"))
    time.sleep(20)