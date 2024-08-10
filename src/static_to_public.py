import os
import shutil


def check_if_folders_exist(static_dir, public_dir):
    if not os.path.exists(static_dir):
        raise ValueError("Static dir is missing")
    if not os.path.exists(public_dir):
        raise ValueError("Public dir is missing")

def wipe_folder(public_dir):
    # Delete everything in public folder
    for filename in os.listdir(public_dir):
        file_path = os.path.join(public_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def recursive_copy(src, dest):
    """
    Copy each file from src dir to dest dir, including sub-directories.
    """
    for item in os.listdir(src):
        file_path = os.path.join(src, item)
        try:
            # if item is a file, copy it
            if os.path.isfile(file_path):
                shutil.copy(file_path, dest)

            # else if item is a folder, recurse 
            elif os.path.isdir(file_path):
                new_dest = os.path.join(dest, item)
                os.mkdir(new_dest)
                recursive_copy(file_path, new_dest)
        except Exception as e:
            print('Failed to copy %s. Reason: %s' % (file_path, e))

def static_to_public():
    path = os.getcwd()
    static_dir = path + "/" + "static"
    public_dir = path + "/" + "public"
    check_if_folders_exist(static_dir, public_dir)
    wipe_folder(public_dir)
    recursive_copy(static_dir, public_dir)

