#!/usr/bin/env python3
#
# SCRIPT: remove_jpeg_duplicates_if_nef_file_exists.py
# AUTHOR: Christophe MICHAUX <chris@cmxconsulting.fr>
# CREATION DATE : 2020-10-08
# WEBSITE : https://www.cmxconsulting.fr
#
# DESCRIPTION : Remove JPEG files if there is a NEF file with the same name in the same directory
#
# Copyright 2020 CMX Consulting
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# If you are searching for other useful scripts, be free to go to https://github.com/cmxconsulting/
#
import os
import hashlib
import sys
import logging
import traceback
import argparse

print("\nRemove JPEG files if there is a NEF file with the same name in the same directory\n")

logger = logging.getLogger('remove_jpeg_duplicates_if_nef_file_exists')
logger.setLevel(logging.INFO)

# create console handler and set level to info
handler = logging.FileHandler('pythonScripts.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

parser=argparse.ArgumentParser()

parser.add_argument('directory', help='The directory to process. For current directory, use "."')

parser.usage = parser.format_help()
try :
    args = parser.parse_args()
except :
    print("\n\nIf you are searching for other useful scripts, be free to go to https://github.com/cmxconsulting/\n\n")
    sys.exit(1)

dirname = args.directory[0]

count = 0
errors = 0

# Process directory passed as parameter
def dup_fileremove(dir):
    duplicate = set()
    os.chdir(dir)
    path=os.getcwd()
    logger.info ("The current directory is: %s" % path)

    for filename in os.listdir(dir):
        filehash = None
        filepath=os.path.join(path, filename)
        filename, file_extension = os.path.splitext(filename)
        if os.path.isdir(filepath):
            dup_fileremove(filepath)
        elif os.path.isfile(filepath) and file_extension.lower() == ".jpg" and (os.path.isfile(filename + ".nef") or os.path.isfile(filename + ".NEF")):
            logger.info("Duplicate entry for %s - Delete file : %s" % (filename, filepath))
            try:
                os.remove(filepath)
                count+=1
            except Exception:
                logger.error('Error while deleting file %s: %s' % (str(filepath), traceback.format_exc()))
                error+=1
    
dup_fileremove(dirname)

print("Operation complete, %d file(s) were removed. %d error(s) found" % (count, errors))
print("If needed, you can read the pythonScripts.log file to have more details\n")
print("If you are searching for other useful scripts, be free to go to https://github.com/cmxconsulting/\n\n")
