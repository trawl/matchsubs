#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random

directory="episodes"
series = ['The.Big.Bang.Theory','Bones','Arrow','Supernatural']
seasons = range(1,2)
episodes = range(1,10)
#versions = ["HDTV.LOL","x264-720p"]
versions = ["HDTV.LOL"]
extensions = ["srt","avi"]
subextra = "subtitle"

baseepformats = ["{}-S{:02}E{:02}-{}.avi","{}.{:01}x{:02}.{}.avi"]
basesubformats = ["{}-S{:02}E{:02}-{}-{}.srt","{}-{:01}x{:02}-{}-{}.srt"]

if not os.path.exists(directory):
  try: os.mkdir(directory)
  except OSError as error: 
    print("OSError: {}".format(error))
    sys.exit(-1)

for name in series:
  for season in seasons:
    for episode in episodes:
      for version in versions:
        
        ename = baseepformats[random.randint(0,1)].format(name,season,episode,version)
        print ("Creating {}...".format(ename))
        open(os.path.join(directory,ename), "a").close()
        
        sname = basesubformats[random.randint(0,1)].format(name,season,episode,version,subextra)
        print ("Creating {}...".format(sname))
        open(os.path.join(directory,sname), "a").close()


