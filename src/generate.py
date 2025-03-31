import os

import shutil

import pathlib

from convert import markdown_to_html_node

def copy_static_to_public(static, public):
    """Copy static files to public directory."""
    if os.path.exists(public):
        shutil.rmtree(public)
    os.mkdir(public)
    static_list = os.listdir(static)
    for item in static_list:
        static_path = os.path.join(static, item)
        print(f"copying {static_path} to public")
        if os.path.isfile(static_path):
            shutil.copy(static_path, public)
        else:
            public_path = os.path.join(public, item)
            os.mkdir(public_path)
            copy_static_to_public(static_path, public_path)

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line.removeprefix("# ")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_f = open(from_path)
    template_f = open(template_path)
    from_text = from_f.read()
    template_text = template_f.read()
    from_f.close()
    template_f.close()
    content = markdown_to_html_node(from_text).to_html()
    title = extract_title(from_text)
    full_HTML = template_text.replace("{{ Title }}", title).replace("{{ Content }}", content).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    dest_f = open(dest_path, "w")
    dest_f.write(full_HTML)
    dest_f.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path[:-2] + "html", basepath)
        return
    items = os.listdir(dir_path_content)
    for item in items:
        generate_pages_recursive(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, item), basepath)
