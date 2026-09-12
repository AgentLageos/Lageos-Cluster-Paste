import os
import sys


def check_args():

    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <file|directory>")
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.isfile(path) and not os.path.isdir(path):
        print(f"File or directory not found: {path}")
        sys.exit(1)

    return path



def collect_files(path):

    files = []

    if os.path.isfile(path):
        files.append(path)

    elif os.path.isdir(path):
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                files.append(os.path.join(root, filename))

    return files

