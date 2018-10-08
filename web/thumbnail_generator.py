from PIL import Image
import os
import time

#Dir to check
main_dir = "./static/images/projects/"
# Subdirectory of main dir
thumbnail_dir = "thumbnails/"
# How often to run, in seconds
script_frequency = 2

def check_files(directory):
    return [f for f in os.listdir(directory)
                     if os.path.isfile(directory + f)]

def update_dir(directory, sizes=[(286, 180), (800, 400)]):
    previous_files = check_files(directory)
    time.sleep(script_frequency)
    new_files = check_files(directory)
    found_files = [f for f in new_files if f not in previous_files]
    print(found_files)
    if len(found_files) > 0:
        for f in found_files:
            print("Found file: " + directory + f + ", making thumbnails...")
            for size in sizes:
                get_thumb(directory, f, size)
    else:
        print("No new files.")
    return update_dir(directory)

def get_thumb(directory, filename, size):
    filename_noend = filename.split(".")[0]
    global thumbnail_dir
    save_file = directory + thumbnail_dir + filename_noend
    save_string = (save_file + "_" + str(size[0]) +
                   "x" + str(size[1]) + ".jpg")
    try:
        with Image.open(directory + filename) as im:
            im.thumbnail(size)
            print("Saving file to: ", save_string)
            im.save(save_string ,"JPEG")
    except FileNotFoundError:
        print("Invalid file.")


update_dir(main_dir)
