#!/usr/bin/env python2.7
#
# SCRIPT: kaamelott_sounds_extract.py 
# AUTHOR: Christophe MICHAUX <chris@cmxconsulting.fr>
# CREATION DATE : 2020-10-08
# WEBSITE : https://www.cmxconsulting.fr
#
# DESCRIPTION : Extract Kaamelott sounds from soundboard website
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
import os
import sys
import logging
import traceback
import argparse
import urllib
import json

print("\nDownload Kaamelott mp3 soundboard.\n")

logger = logging.getLogger('kaamelott')
logger.setLevel(logging.INFO)

# create console handler and set level to info
handler = logging.FileHandler('pythonScripts.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

parser = argparse.ArgumentParser()

parser.add_argument('directory', help='The directory to output MP3 files. For current directory, use "."')

parser.usage = parser.format_help()
try:
    args = parser.parse_args()
except:
    print("\n\nIf you are searching for other useful scripts, be free to go to https://github.com/cmxconsulting/\n\n")
    sys.exit(1)

dirname = args.directory
print "dir : %s" % dirname
count = 0
errors = 0

os.chdir(dirname)



def open_json(destDir):
    print"Get Kaamelott sounds"
    url = "https://kaamelott-soundboard.2ec0b4.fr/sounds/sounds.98d7c898.json"
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    for keyval in data:
        download_file(destDir, keyval["file"])


def download_file(destDir, sound):
    global count
    print "Download file : %s" % sound
    testfile = urllib.URLopener()
    outputDir = "%s/%s" % (destDir, sound)
    print"output dir : %s" % outputDir
    testfile.retrieve("https://kaamelott-soundboard.2ec0b4.fr/sounds/%s" % sound, outputDir)
    count += 1

print "Dirname : %s" % dirname
open_json(dirname)

print("Operation complete, %d file(s) were downloaded. %d error(s) found" % (count, errors))
print("If needed, you can read the pythonScripts.log file to have more details\n")
print("If you are searching for other useful scripts, be free to go to https://github.com/cmxconsulting/\n\n")
