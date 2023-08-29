import sys
import os
sys.path.append(os.getcwd())
from jsonCompare import compareJSON_Utils

if __name__ == '__main__':
    file_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(file_path)

    compareJSON_Utils().runThisFolder(dir_path)