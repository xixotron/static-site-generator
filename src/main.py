import os
import shutil
import sys

from copytree import copy_tree
from gencontent import generate_pages_recursive


def main():
    basepath = "/"
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]

    print(basepath)
    public_path = "./docs"
    static_path = "./static"
    content_path = "./content"
    template_path = "./template.html"

    if not os.path.exists(static_path):
        raise FileNotFoundError(f"Static directory '{static_path}' not found")

    print("Removing public folder...")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    print("copying static folder to public folder")
    copy_tree(static_path, public_path)


    print("Generatin from content...")
    generate_pages_recursive(content_path, template_path, public_path, basepath)


if __name__ == "__main__":
    main()
