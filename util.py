import sys
import collections


def my_print(str, file=sys.stdout):
    if file is None:
        return
    if isinstance(file, list):
        for f in file:
            print(str, file=f)
    else:
        print(str, file=file)
