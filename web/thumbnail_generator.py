from PIL import Image
import os
import time

#Dir to check
main_dir = "./static/images/projects/"
# Subdirectory of main dir
thumbnail_dir = "thumbnails/"
# How often to run, in seconds
script_frequency = 2
# Format string of new file
save_string =  lambda f, directory, size: (directory +
                                            f[0] + "_" + str(size[0]) +
                                            "x" + str(size[1]) + "." + f[1])

def check_files(directory):
    """ Returns every file in a directory without
    its file suffix."""
    return [f.split(".") for f in os.listdir(directory)
                     if os.path.isfile(directory + f)]

def update_dir(directory, sizes=[(286, 180), (800, 400)]):
    """ Checks that every file in a given directory has
    thumbnails generated in its subfolder, the global variable
    thumbnails_dir."""
    files = check_files(directory)
    # Uncomment next line if running script standalone
    time.sleep(script_frequency)
    for f in files:
        for size in sizes:
            if not os.path.isfile(save_string(f, directory+thumbnail_dir, size)):
                print("File: " + directory + ".".join(f)
                      + " does not have a thumbnail,generating size: " + str(size))
                get_thumb(directory, f, size)
    else:
        print("No new thumbnails to generate.")
    return update_dir(directory)

def get_thumb(directory, filename, size):
    global thumbnail_dir
    try: 
        with Image.open(directory + ".".join(filename) ) as im:
            # Convert to thumbnail
            im.thumbnail(size)
            print("Saving file to: ",
                  save_string(filename, directory +
                              thumbnail_dir, size))
            im.save(save_string(filename,
                                directory + thumbnail_dir, size),
                    im.format)
    except FileNotFoundError:
        print("File not found.")
    except IOError:
        pass


update_dir(main_dir)
