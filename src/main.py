import os

import shutil

from textnode import *

def copy_static_to_public(static, public):
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

def main():
    copy_static_to_public("static","public")

main()