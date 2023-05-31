import os
import sys
import shutil
import platform
import py7zr
import requests
from zipfile import ZipFile
from colorama import Fore


DOWNLOAD_URLS = {
    "raMain": "https://buildbot.libretro.com/nightly/nintendo/wiiu/RetroArch_rpx.7z",
    "raAssets": "https://buildbot.libretro.com/assets/frontend/assets.zip",
    "raCheats": "https://buildbot.libretro.com/assets/frontend/cheats.zip",
    "raShaders": "https://buildbot.libretro.com/assets/frontend/shaders_slang.zip",
    "gb": "https://archive.org/download/dmg_rom/dmg_rom.bin",
    "gbc": "https://archive.org/download/cgb_boot/cgb_boot.bin",
    "gba": "http://download2330.mediafire.com/88aqhp6prorgDsB4f5ogsnky3ebyRwrTidaXK7O6hx5TZb5PwJglVKUy0Pq2KooDPbfwcNqGg1PH3VUe7xnj5Almp4dIaJ225W6m3i-61OCZxOOD_pnLuaYZIWvtY30SFJOPpq_h20t4X4p9jCp7cScmmsiRQFUDH75McXh7ufXGEg/uijj3i3349h8j2j/gba_bios.zip",
}


cwd = os.getcwd()
tmp_path = os.path.join(cwd, "tmp")
copy_to_sd_path = os.path.join(cwd, "copy-to-sd-card")


def clear():
    return os.system("clear")


def extract_7z(file_name, path=tmp_path):
    with py7zr.SevenZipFile(file_name) as archive:
        archive.extractall(path=path)


def extract_zip(file_name, path=tmp_path):
    with ZipFile(file_name) as archive:
        archive.extractall(path=path)


def download(url, file_name, path=tmp_path):
    file_path = os.path.join(path, file_name)
    response = requests.get(url, stream=True)
    response.raise_for_status()

    length = response.headers.get("content-length")
    block_size = 131072
    if length:
        length = int(length)
        block_size = max(4096, length // 20)

    filesize = round(int(length) * 10**-6, 2)
    print(Fore.BLUE + f"{file_name}" + Fore.RESET + " size: " + Fore.CYAN + f"{filesize} MB" + Fore.RESET)

    with open(file_path, "wb") as f:
        size = 0
        for buffer in response.iter_content(block_size):
            if not buffer:
                break
            f.write(buffer)
            size += len(buffer)
            if length:
                percent = int((size / length) * 100)
                print(Fore.RESET + "Downloading " + Fore.BLUE + f"{file_name}" + ": " + Fore.CYAN + f"{percent}%", end="\r")

    print(Fore.GREEN + "\n\nDone Downloading: " + Fore.CYAN + f"{file_name}" + Fore.RESET + "\n")


def setup_directories():
    if not os.path.isdir(tmp_path):
        os.mkdir(tmp_path)
    if not os.path.isdir(copy_to_sd_path):
        os.mkdir(copy_to_sd_path)


def main():
    clear()
    setup_directories()

    prompt = input("\033[1;37mRetroArch Wii U Setup Tool\n\033[0;0mType the number of the corresponding option that you want to select.\n1. Download/Update the main RetroArch files.\n2. Download/Update RetroArch Core Bios Files.\n3. Download/Update RetroArch Cheat Files.\n4. Download/Update RetroArch Shaders.\n5. Exit tool\n\nOption: ")

    if prompt == "1":
        clear()
        print("Starting Download of Base RetroArch Files.\n")
        download(DOWNLOAD_URLS["raMain"], "retroarch-wiiu.7z")
        print("Extracting retroarch-wiiu.7z")
        extract_7z(os.path.join(tmp_path, "retroarch-wiiu.7z"))
        # Not adding the rest of this as this is an example

    elif prompt == "2":
        clear()
        print("Starting Downloadof Core Bios Files.\n")
        download(DOWNLOAD_URLS["gb"], "gb_bios.bin")
        download(DOWNLOAD_URLS["gbc"], "gbc_bios.bin")
        download(DOWNLOAD_URLS["gba"], "gba_bios.zip")
        print("Extracting gba_bios.zip")
        extract_zip(os.path.join(tmp_path, "gba_bios.zip"))
        # Not adding the rest of this as this is an example

    elif prompt == "3":
        clear()
        print("Starting Download of Cheat Files.\n")
        download(DOWNLOAD_URLS["raCheats"], "cheats.zip")
        print("Extracting cheats.zip")
        extract_zip(os.path.join(tmp_path, "cheats.zip"))
        # Not adding the rest of this as this is an example

    elif prompt == "4":
        clear()
        print("Starting Download of Shaders.\n")
        download(DOWNLOAD_URLS["raShaders"], "shaders_slang.zip")
        print("Extracting shaders_slang.zip")
        extract_zip(os.path.join(tmp_path, "shaders_slang.zip"))
        # Not adding the rest of this as this is an example

    elif prompt == "5":
        print("Exiting...")
        sys.exit(0)

    else:
        print("Invalid option. Please try again.")
        main()


if __name__ == "__main__":
    main()
