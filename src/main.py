from generate import *

import sys

def main():
    copy_static_to_public("static","docs")
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    generate_pages_recursive("content", "template.html", "docs", basepath)
main()