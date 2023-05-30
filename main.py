import requests, os, sys, shutil, platform, py7zr
from colorama import Fore; from zipfile import ZipFile

#* main download urls
raMain = 'https://buildbot.libretro.com/nightly/nintendo/wiiu/RetroArch_rpx.7z'
raAssets = 'https://buildbot.libretro.com/assets/frontend/assets.zip'
raCheats = 'https://buildbot.libretro.com/assets/frontend/cheats.zip'
raAutoconfig = 'https://buildbot.libretro.com/assets/frontend/autoconfig.zip'
raDataRDB = 'https://buildbot.libretro.com/assets/frontend/database-rdb.zip'
raInfo = 'https://buildbot.libretro.com/assets/frontend/info.zip'
raOverlays = 'https://buildbot.libretro.com/assets/frontend/overlays.zip'
raShaders = 'https://buildbot.libretro.com/assets/frontend/shaders_slang.zip'
gb = 'https://archive.org/download/dmg_rom/dmg_rom.bin'
gba = 'http://download2330.mediafire.com/88aqhp6prorgDsB4f5ogsnky3ebyRwrTidaXK7O6hx5TZb5PwJglVKUy0Pq2KooDPbfwcNqGg1PH3VUe7xnj5Almp4dIaJ225W6m3i-61OCZxOOD_pnLuaYZIWvtY30SFJOPpq_h20t4X4p9jCp7cScmmsiRQFUDH75McXh7ufXGEg/uijj3i3349h8j2j/gba_bios.zip'
gbc = 'https://archive.org/download/cgb_boot/cgb_boot.bin'
# os check function
cwd = os.getcwd()
tmp = os.path.isdir(cwd+'/tmp')
#if tmp != False:
#    shutil.rmtree('tmp')
flavor = platform.platform(terse=True)
username = os.path.expanduser('~')
if tmp !=True:
    os.mkdir(cwd+'/tmp')
# clear function
def clear():
    return(os.system('clear'))

# 7z extract function
def extract7z(fileName: str, path = cwd+'/tmp'):
    extract = py7zr.SevenZipFile(fileName)
    return(extract.extractall(path='tmp'))

# zip extract function
def extractZIP(fileName: str, path = cwd+'/tmp'):
    extract = ZipFile(fileName)
    return(extract.extractall(path=path))

#* Download Function
def download(url, fileName, path='tmp/'):
    exists = os.path.isfile(path+fileName)
    if exists == True:
        print('\n'+Fore.RED+'⚠️Warning⚠️ '+Fore.CYAN+fileName+Fore.RESET+' is already downloaded'+Fore.YELLOW+' SKIPPING Download.'+Fore.RESET)
        return()
    response = requests.get(url, stream=True)
    response.raise_for_status()
    length = response.headers.get('content-length')
    block_size = 1000000  # default value
    if length:
        length = int(length)
        block_size = max(4096, length // 20)
    filesize = length*10**-6
    filesize = round(filesize, 2)
    print(Fore.BLUE+f"{fileName}"+Fore.RESET+' size: '+Fore.CYAN+f"{filesize} MB"+Fore.RESET)
    with open(path+fileName, 'wb') as f:
        size = 0
        for buffer in response.iter_content(block_size):
            if not buffer:
                break
            f.write(buffer)
            size += len(buffer)
            if length:
                percent = int((size / length) * 100)
                print(Fore.RESET+"Downloading "+Fore.BLUE+f"{fileName}"+': '+Fore.CYAN+f"{percent}%", end='\r')
    print(Fore.GREEN+"\n\nDone Downloading: "+Fore.CYAN+f"{fileName}"+Fore.RESET+'\n')

#* Main Function

clear()

# prompt for entire program

prompt = input('\033[1;37mRetroArch Wii U Setup Tool\n\033[0;0mType the number of the corrasponding option that you want to select.\n1. Download/Update the main RetroArch files.\n2. Download/Update RetroArch Core Bios Files.\n3. Download/Update RetroArch Cheat Files.\n4. Download/Update RetroArch Shaders.\n5. Exit tool\n\nOption: ')

if prompt == '1':
    clear()
    print('Starting Download of Base RetroArch Files.\n')
    download(raMain, 'retroarch-wiiu.7z')
    print('Extracting retroarch-wiiu.7z')
    extract7z('tmp/retroarch-wiiu.7z')
    os.chdir('tmp/wiiu/apps/')
    appDir = os.path.isdir(cwd+'/tmp/ra')
    assetsDir = os.path.isdir(cwd+'/tmp/retroarch/assets')
    if assetsDir == True:
        shutil.rmtree(cwd+'/tmp/retroarch/assets')
        download(url=raAssets, fileName='assets.zip', path=cwd+'/tmp/')
        extractZIP(cwd+'/tmp/assets.zip',path= cwd+'/tmp/assets/')
        os.remove(cwd+'/tmp/assets.zip')
        shutil.move(cwd+'/tmp/assets', cwd+'/tmp/retroarch/assets')
    if appDir == False:
        shutil.copytree(cwd+'/tmp/wiiu/apps/retroarch',cwd+'/tmp/ra/')
        shutil.rmtree(cwd+'/tmp/wiiu/apps')
        os.mkdir(cwd+'/tmp/wiiu/apps')
        shutil.copytree(cwd+'/tmp/ra',cwd+'/tmp/wiiu/apps/retroarch/')
        shutil.rmtree(cwd+'/tmp/ra')
    dlDir = os.path.isdir(cwd+'/copy-to-sd-card')
    raDir = os.path.isdir(cwd+'/copy-to-sd-card/retroarch')
    wiiuDir = os.path.isdir(cwd+'/copy-to-sd-card/wiiu')
    if dlDir == False:
        os.mkdir(cwd+'/copy-to-sd-card')
    if raDir == False:
        shutil.copytree(cwd+'/tmp/retroarch',cwd+'/copy-to-sd-card/retroarch/')
        shutil.rmtree(cwd+'/tmp/retroarch')
    if wiiuDir == False:
        shutil.copytree(cwd+'/tmp/wiiu',cwd+'/copy-to-sd-card/wiiu/')
        shutil.rmtree(cwd+'/tmp/wiiu')
    os.remove(cwd+'/tmp/retroarch-wiiu.7z')
    print('Done Installing base retroarch files')

if prompt == '2':
    clear()
    print('Starting Download of RetroArch Core Bios Files.')
    download(gb, fileName='dmg_rom.bin', path=cwd+'/tmp/')
    download(gbc, fileName='cgb_boot.bin',path=cwd+'/tmp/')
    download(gba, fileName='gba_bios.zip',path=cwd+'/tmp/')
    extractZIP(cwd+'/tmp/gba_bios.zip')
    os.remove(cwd+'/tmp/gba_bios.zip')
    copydir = os.path.isdir(cwd+'/copy-to-sd-card')
    if copydir == False:
        os.mkdir(cwd+'/copy-to-sd-card')
        os.mkdir(cwd+'/copy-to-sd-card/retroarch')
        os.mkdir(cwd+'/copy-to-sd-card/retroarch/cores')
        os.mkdir(cwd+'/copy-to-sd-card/retroarch/cores/system')
        shutil.copytree(cwd+'/tmp',cwd+'/copy-to-sd-card/retroarch/cores/system')
    else:
        os.rmdir(cwd+'/copy-to-sd-card/retroarch/cores/system')
        shutil.copytree(cwd+'/tmp/',cwd+'/copy-to-sd-card/retroarch/cores/system/')
    shutil.rmtree(cwd+'/tmp')
if prompt == '3':
    clear()
    download(raCheats,fileName='cheats.zip',path=cwd+'/tmp/')
    extractZIP(cwd+'/tmp/cheats.zip',cwd+'/tmp/cheats')
    copydir = os.path.isdir(cwd+'/copy-to-sd-card')
    if copydir == False:
        os.mkdir(cwd+'/copy-to-sd-card')
        os.mkdir(cwd+'/copy-to-sd-card/retroarch')
        os.mkdir(cwd+'/copy-to-sd-card/retroarch/cht')
        shutil.copytree(cwd+'/tmp/cheats/',cwd+'/copy-to-sd-card/retroarch/cht/')
    else:
        shutil.copytree(cwd+'/tmp/cheats',cwd+'/copy-to-sd-card/retroarch/cht/')
    shutil.rmtree(cwd+'/tmp')
if prompt == '4':
    clear()
    download(raShaders, 'shaders.zip')
    extractZIP(cwd+'/tmp/shaders.zip', path=cwd+'/tmp/shaders')
    copydir = os.path.isdir(cwd+'/copy-to-sd-card')
    if copydir == False:
        os.mkdir(cwd+'/copy-to-sd-card')
        os.mkdir(cwd+'/copy-to-sd-card/retroarch')
        os.mkdir(cwd+'/copy-to-sd-card/retroarch/shaders')
        shutil.copytree(cwd+'/tmp/shaders',cwd+'/copy-to-sd-card/retroarch/shaders/')
    else:
        shutil.copytree(cwd+'/tmp/shaders',cwd+'/copy-to-sd-card/retroarch/shaders/')
    shutil.rmtree(cwd+'/tmp')
if prompt == '5':
    clear()
    sys.exit('Closing the tool...')

