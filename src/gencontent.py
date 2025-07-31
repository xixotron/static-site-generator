import os
import re


from markdown_to_html import markdown_to_html_node

def generate_pages_recursive(dir_path_content : str, template_path : str, dest_dir_path :str):
    print(f"generate_pages_recursive({dir_path_content}, {template_path}, {dest_dir_path})")

    if not os.path.exists(dest_dir_path):
        print(f"Folder {dest_dir_path} not found, creating ...")
        os.mkdir(dest_dir_path)

    for file in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)

        if os.path.isfile(from_path) and file.endswith(".md"):
            html_file = file.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, html_file)
            generate_page(from_path, template_path, dest_path)
        elif os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_path)


def generate_page(from_path : str, template_path : str, dest_path : str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", content)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    with open(dest_path, "w") as f:
        f.write(page)


def extract_title(markdown: str) -> str:
    matches = re.findall(r"^# ([^\n]*)$", markdown, re.MULTILINE)
    if not matches:
        raise Exception("Header not found")
    return matches[0]

