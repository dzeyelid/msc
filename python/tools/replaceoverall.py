#!/usr/bin/env python
# coding: utf-8

import sys
import os
import glob
import codecs
from datetime import datetime

def replace_word(file_path, replace_from, replace_to):

    word_from = replace_from.decode('shift_jis')
    word_to = replace_to.decode('shift_jis')
#    print 'from = ', word_from
#    print 'to = ', word_to

    file_path_temp = file_path + '.temp'

    file_orig = codecs.open(file_path, 'r', 'shift_jis')
    file_temp = codecs.open(file_path_temp, 'w', 'shift_jis')
    replace_num = 0

    try:
        for line in file_orig:
            line_dest = line.replace(word_from, word_to)
            file_temp.write(line_dest)
            if line != line_dest:
#                print '>>', line_dest
                replace_num += 1
    except UnicodeDecodeError:
        print 'UnicodeDecodeError : ', file_path
        replace_num = 0

    finally:
        file_orig.close()
        file_temp.close()

        if 0 < replace_num:
            if not os.access(file_path, os.W_OK):
                os.chmod(file_path, 0777)

            d = datetime.today()
            file_path_old = file_path + '.' + d.strftime("%y%m%d%H%M%S") + '.old'
            os.rename(file_path, file_path_old)
            os.rename(file_path_temp, file_path)

        if os.path.exists(file_path_temp):
            os.remove(file_path_temp)

    return replace_num


if __name__ == '__main__':

    replace_from = None
    replace_to = None
    target_path = os.getcwd()

    if len(sys.argv) <= 1:
        print "Please give words to replace."
        print "$ python replaceoverall.py [replace_from] [replace_to] [target path]"
        sys.exit(2)

    if 1 < len(sys.argv):
        replace_from = sys.argv[1]
    if 2 < len(sys.argv):
        replace_to = sys.argv[2]
    if 3 < len(sys.argv):
        target_path = sys.argv[3]
        
    for dirpath, dirs, files in os.walk(target_path):
        for each_file in files:
            if each_file.endswith('.cpp'):
                file_path = os.path.join(dirpath, each_file)
                replace_num = replace_word(file_path, replace_from, replace_to)
                if 0 < replace_num:
                    print replace_num, "words were replaced.\t", file_path
