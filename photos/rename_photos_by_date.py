#!/usr/bin/env python3
#
# SCRIPT: rename_photos_by_date.py
# AUTHOR: Christophe MICHAUX <chris@cmxconsulting.fr>
# CREATION DATE : 2020-10-08
# WEBSITE : https://www.cmxconsulting.fr
#
# DESCRIPTION : Rename the photos by their shot date.
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
# Install :
# pip install exifread
try :
    import os
    import hashlib
    import sys
    import logging
    import traceback
    import exifread
    import argparse
except :
    print("Please launch these commands before launching this script : ")
    print("    pip3 install exifread")
    print("If you have some problems with this pip3 command, try to launch : ")
    print("pip3 --trusted-host pypi.org --trusted-host files.pythonhosted.org install exifread")
    sys.exit(2)

print("\nRename the photos by their shot date.\n")

logger = logging.getLogger('renamePhotosByDate')
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

os.chdir(dirname)

def get_date_taken(path):
    return Image.open(path)._getexif()[36867]
    
def process_rename(dir):
    
    os.chdir(dir)
    path=os.getcwd()
    logger.info ("The current directory is: %s" % path)
    
    for filename in os.listdir(dir):
        filehash = None
        filepath=os.path.join(dir, filename)
        filename, file_extension = os.path.splitext(filename)
        if os.path.isfile(filepath) and filename.startswith('DSC') :
            try:
                logger.info("File to rename : %s" % filepath)
                logger.debug("File %s - Date : %s", (filepath, get_date_taken(filepath)))
                
                f = open(filepath, 'rb')
                exif = exifread.process_file(f)
                
                dt = str(exif['EXIF DateTimeOriginal'])  # might be different
                # segment string dt into date and time
                day, dtime = dt.split(" ", 1)
                # segment time into hour, minute, second
                hour, minute, second = dtime.split(":", 2)
                
                name=day.replace(":", "-")
                
                target=os.path.join(dir, name+file_extension)
                idx=2
                while (os.path.isfile(target)):
                    target=os.path.join(dir, name+"_"+str(idx)+file_extension)
                    idx+=1
                
                print("Rename file %s to %s " % (filename, target))
                
                f.close()                
                # Rename here
                os.rename(filepath, target)
                count +=1 
            except Exception:
                logger.error('Error while processing file %s: %s' % (str(filepath), traceback.format_exc()))
                error +=1 

process_rename(dirname)

print("Operation complete, %d file(s) were removed. %d error(s) found" % (count, errors))
print("If needed, you can read the pythonScripts.log file to have more details\n")
print("If you are searching for other useful scripts, be free to go to https://github.com/cmxconsulting/\n\n")
