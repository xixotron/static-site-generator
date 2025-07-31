import os
import shutil

from textnode import *
from md_parser import extract_markdown_links, split_nodes_delimiter, extract_markdown_images, split_nodes_link

def main():
    cwd = os.getcwd()
    print(f"{cwd=}")

    copy_static_to_to_public(cwd)

def copy_static_to_to_public(cwd):
    static_path = os.path.join(cwd, "static")
    public_path = os.path.join(cwd, "public")
    if not os.path.exists(static_path):
        raise FileNotFoundError(f"Static route: '{static_path}' not found")

    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    os.mkdir(public_path)

    copy_tree(static_path, public_path)

def copy_tree(src, dst):
    folders = ["."]
    while len(folders) > 0:
        cur_dir = folders.pop(0)
        print(f"folder {cur_dir}:")
        src_path = os.path.join(src, cur_dir)
        dst_path = os.path.join(dst, cur_dir)
        copy_files_in_folder(src_path, dst_path)

        for file in os.listdir(src_path):
            partial_file_path = cur_dir + "/" + file
            file_path = os.path.join(src, partial_file_path)
            if os.path.isdir(file_path):
                folders.append(partial_file_path)


def copy_files_in_folder(src, dst):
    for file in os.listdir(src):
        src_path = os.path.join(src, file)
        dst_path = os.path.join(dst, file)
        if os.path.isfile(src_path):
            print(f"Copy: '{src_path}' to '{dst_path}'")
            shutil.copy(src_path, dst_path)


if __name__ == "__main__":
    main()
    print("hello world")
