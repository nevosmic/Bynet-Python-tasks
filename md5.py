#! /bin/python3
import time
from multiprocessing import Pool
import getopt
import sys
from os import scandir, walk
from os.path import isfile, join, isdir
import hashlib
from multiprocessing import Pool


def md5(fname):
    """Note that sometimes you won't be able to fit the whole file in memory.
    In that case, read chunks of 4096 bytes sequentially and feed them to the md5 method"""
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def print_files_in_directory(path):
    """ Using scandir() instead of listdir() can significantly increase the performance
    of code that also needs file type or file attribute information """
    count_files = 0
    with scandir(path) as iterator:
        for entry in iterator:
            if entry.is_file():
                count_files += 1
                print('{}, {}, {}'.format(count_files, entry.name, md5(entry)))

    if count_files == 0:
        print('No files in {}'.format(path))


if __name__ == '__main__':
    """ if number of arguments is more than 3 or less than 2 - not valid
     (note that argument 0 is the script name) 
     If second argument is not a directory - not valid """
    is_multi = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "m", ["multi-process"])
    except getopt.GetoptError as err:
        print(err)  # will print something like "option -a not recognized"
        exit(2)
    for opt, arg in opts:
        if opt in ('-m', '--multi-process'):
            is_multi = True

    if len(sys.argv) > 3:
        print('Too many arguments, please enter a path to a directory, '
              'you can add [-m] flag for multi processing before it')
        exit(1)
    elif len(sys.argv) < 2:
        print('Missing arguments, please enter a path to a directory,'
              ' you can add [-m] flag for multi processing before it')
        exit(1)
    input_dir = sys.argv[-1]
    if isdir(input_dir):
        if is_multi:
            t1 = time.time()
            p = Pool()
            p.map(print_files_in_directory, [input_dir])
            p.close()
            p.join()
            print('Pool took:', time.time() - t1)
        else:
            t2 = time.time()
            print_files_in_directory(input_dir)
            print('Normal took:', time.time() - t2)
    else:
        print('{} is not a directory, please enter a valid directory path'.format(input_dir))
        exit(1)

