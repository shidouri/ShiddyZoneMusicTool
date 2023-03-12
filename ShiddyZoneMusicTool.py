from tkinter import Tk
from tkinter import simpledialog
from tkinter.filedialog import askopenfilenames
from tkinter import messagebox
from datetime import datetime
import os
from time import sleep


def OPEN_FILE_NAMES_ROUND_START():
    
    filenames = askopenfilenames(title="Open Round START Files", filetypes=[('Round START WAV Files(NOT END!)','*.wav')])

    try:
        for name in filenames:
            if 'sound_assets' not in name: return None
        
        return filenames
    
    except:
        return None

def OPEN_FILE_NAMES_ROUND_END():
    
    filenames = askopenfilenames(title="Open Round END Files", filetypes=[('Round END WAV Files(NOT START!)','*.wav')])

    try:
        for name in filenames:
            if 'sound_assets' not in name: return None
        
        return filenames
    
    except:
        return None


def SPLIT_WAV_PATHS(file_paths):
    
    return_paths = []
    temp_array = []
    
    for path in file_paths:
        temp_array = path.split('/sound_assets/')
        return_paths.append(temp_array[len(temp_array)-1] )
        
    return return_paths
        
    

def main():
    
    gsc_out_string_roundstart = ''
    gsc_out_string_roundend = ''
    csv_alias_string_array = []
    current_dir = os.getcwd()
    rootTK = Tk()
    rootTK.withdraw()
    rootTK.title("ShiddyZoneMusicTool")
    rootTK.after(1, lambda: rootTK.focus_force())
    try: this_zone = simpledialog.askstring(title = "ShiddyZoneMusicTool v1.0     ", prompt = "Enter the zone name to generate for [ie start_zone]           ", initialvalue="start_zone")
    except: 
        print("No zone selected! You silly sausage!")
        sleep(5)
        return
        
    if this_zone is None or this_zone == "": 
        print("No zone selected! You silly sausage!")
        sleep(5)
        return
        
    try: round_start = OPEN_FILE_NAMES_ROUND_START()
    except:
        print("Sound assets must be in BO3/sound_assets!\n") 
        sleep(5)
        return
    
    if round_start is None: 
        print("Sound assets must be in BO3/sound_assets!\n")
        sleep(5)
        return

    try:
        split_round_start_wavpaths = SPLIT_WAV_PATHS(round_start)
    
    except:
        print("Failed to split wavpaths!\n")
        sleep(5)
        return
    
    if split_round_start_wavpaths is None:
        print("Failed to split wavpaths!\n")
        sleep(5)
        return
    
    round_start_alias_dict = {}
    
    for path in split_round_start_wavpaths:
        path_alias = simpledialog.askstring(title = "Enter aliasname...          ", prompt = f"Enter alias for {path}...          ", parent= rootTK)
        if path_alias is None or path_alias == "":
            print("Alias cannot be empty!\n")
            sleep(5)
            return
        else: round_start_alias_dict[path_alias] = path


    try: round_end = OPEN_FILE_NAMES_ROUND_END() 
    except:
        print("Sound assets must be in BO3/sound_assets!\n")
        sleep(5)
        return
    
    if round_end is None: 
        print("Sound assets must be in BO3/sound_assets!\n")
        sleep(5)    
        return

    try:
        split_round_end_wavpaths = SPLIT_WAV_PATHS(round_end)
    
    except:
        print("Failed to split wavpaths!\n")
        sleep(5)
        return
    
    if split_round_end_wavpaths is None:
        print("Failed to split wavpaths!\n")
        sleep(5)
        return
    
    round_end_alias_dict = {}
    
    for path in split_round_end_wavpaths:
        path_alias = simpledialog.askstring(title = "Enter aliasname...          ", prompt = f"Enter alias for {path}...          ")
        if path_alias is None or path_alias == "":
            return
        else: round_end_alias_dict[path_alias] = path
    

    now = datetime.now()
    dt_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    
    if not os.path.exists(f"{current_dir}\\outfiles"):
        os.mkdir(f"{current_dir}\\outfiles")
    if not os.path.exists(f"{current_dir}\\backup"):
        os.mkdir(f"{current_dir}\\backup")
        
    outfile_path = fr"{current_dir}\outfiles\{this_zone}.txt"
    outfile_backup_path = fr"{current_dir}\backup\{dt_str}__{this_zone}.bak.txt"

    
    for key in round_start_alias_dict:
       gsc_out_string_roundstart += ('"'+ key + '",')
    
    for key in round_end_alias_dict:
       gsc_out_string_roundend += ('"'+ key + '",')
        
    start_round_gsc_line = rf'level.a_location_round_sound_begin["{this_zone}"] = array( {gsc_out_string_roundstart[:-1]} );'
    end_round_gsc_line = rf'level.a_location_round_sound_end["{this_zone}"] = array( {gsc_out_string_roundend[:-1]} );'


    for key in round_start_alias_dict:
        fixed_wavstr = round_start_alias_dict[key].replace(r'/', '\\')
        
        csv_alias_string_array.append(f'{key},,,{fixed_wavstr},,,UIN_MOD,,,,,BUS_MUSIC,grp_music,,,,,100,100,,,,,,,,,,,,,,100,100,0,1,,2d,music_all,,NONLOOPING,,,,,,,,,,,,,,,,,,,,,,,yes,,,,yes,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n')

    for key in round_end_alias_dict:
        fixed_wavstr = round_end_alias_dict[key].replace(r'/', '\\')
        csv_alias_string_array.append(f'{key},,,{fixed_wavstr},,,UIN_MOD,,,,,BUS_MUSIC,grp_music,,,,,100,100,,,,,,,,,,,,,,100,100,0,1,,2d,music_all,,NONLOOPING,,,,,,,,,,,,,,,,,,,,,,,yes,,,,yes,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n')


    with open(outfile_path, "w") as f:
        f.writelines("//GSC lines for zm_zone_specific_round_sounds:\n\n")
        f.writelines(start_round_gsc_line)
        f.writelines("\n")
        f.writelines(end_round_gsc_line)
        f.writelines("\n\n\n\n")
        f.writelines("#Block to add to the alias csv:\n")
        f.writelines(csv_alias_string_array)
    
    with open(outfile_backup_path, "w") as f:
        f.writelines("//GSC lines for zm_zone_specific_round_sounds:\n\n")
        f.writelines(start_round_gsc_line)
        f.writelines("\n")
        f.writelines(end_round_gsc_line)
        f.writelines("\n\n\n\n")
        f.writelines("#Block to add to the alias csv:\n")
        f.writelines(csv_alias_string_array)
    
    messagebox.showinfo(title="Done!", message=f"GSC lines and CSV aliases written to {outfile_path}")
    print(f"GSC lines and CSV aliases written to\n{outfile_path}\nand also to\n{outfile_backup_path}\n\n" +
          "This window will close at some point if you don't close it yourself.\n" +
          "If you used this tool and found it useful, let me know on Discord! :D\n")
    
    sleep(8)
    return
    
main()
