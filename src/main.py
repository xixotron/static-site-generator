import os
import shutil

def main():
    cwd = os.getcwd()
    print(f"{cwd=}")

    copy_static_to_to_public(cwd)


def copy_static_to_to_public(cwd):
    static_path = os.path.join(cwd, "static")
    public_path = os.path.join(cwd, "public")
    if not os.path.exists(static_path):
        raise FileNotFoundError(f"Static directory '{static_path}' not found")

    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    copy_tree(static_path, public_path)


def copy_tree(src, dst):
    print(f"copy_tree('{src}', '{dst}')")
    if not os.path.exists(dst):
        os.mkdir(dst)

    for file in os.listdir(src):
        src_path = os.path.join(src, file)
        dst_path = os.path.join(dst, file)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"copying: '{src_path}' to '{dst_path}'")

        elif os.path.isdir(src_path):
            copy_tree(src_path, os.path.join(dst, file))


if __name__ == "__main__":
    main()
