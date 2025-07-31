import os
import shutil


def copy_tree(src, dst):
    print(f"copy_tree('{src}', '{dst}')")
    if not os.path.exists(dst):
        os.mkdir(dst)

    for file in os.listdir(src):
        src_path = os.path.join(src, file)
        dst_path = os.path.join(dst, file)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f" * '{src_path}' -> '{dst_path}'")

        elif os.path.isdir(src_path):
            copy_tree(src_path, os.path.join(dst, file))

