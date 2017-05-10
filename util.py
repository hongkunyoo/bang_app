import sys


def my_print(str, file=sys.stdout):
    if file is None:
        return
    if isinstance(file, list):
        for f in file:
            print(str, file=f)
    else:
        print(str, file=file)


def close_file(f):
    if f is not None:
        f.close()
