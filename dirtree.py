#! /bin/python3

import getopt
import sys
from os import scandir, walk
from os.path import isfile, join, isdir


def print_files_in_directory(path):
    """ Using scandir() instead of listdir() can significantly increase the performance
    of code that also needs file type or file attribute information """
    count_files = 0
    with scandir(path) as iterator:
        for entry in iterator:
            if entry.is_file():
                count_files += 1
                print(entry.name)

    if count_files == 0:
        print('No files in {}'.format(path))


def print_files_in_directory_rec(path):
    for current_path, folders, files in walk(path):
        for file in files:
            print(join(current_path, file))


if __name__ == '__main__':
    """ if number of arguments is more than 3 or less than 2 - not valid
     (note that argument 0 is the script name) 
     If second argument is not a directory - not valid """
    is_rec = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "r", ["recursive"])
    except getopt.GetoptError as err:
        print(err)  # will print something like "option -a not recognized"
        exit(2)
    for opt, arg in opts:
        if opt in ('-r', '--recursive'):
            is_rec = True

    if len(sys.argv) > 3:
        print('Too many arguments, please enter a path to a directory first you can add [-r] flag for recursive')
        exit(1)
    elif len(sys.argv) < 2:
        print('Missing arguments, please enter a path to a directory first you can add [-r] flag for recursive')
        exit(1)
    input_dir = sys.argv[-1]
    if isdir(input_dir):
        if is_rec:
            print_files_in_directory_rec(input_dir)
        else:
            print_files_in_directory(input_dir)
    else:
        print('{} is not a directory, please enter a valid directory path'.format(input_dir))
        exit(1)


