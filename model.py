#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import difflib

class EpisodeFile():
    
    TYPES = {'episode':('.avi','.mp4','.mkv'),'subtitle':('.srt','.sub')}
    
    def __init__(self,filename=""):
        self.filename =    filename
        self.series = ""
        self.season = -1
        self.number = -1
        self.version = ""
        self.filetype = ""
        self.extension = ""
        if not self._process():
            raise ValueError("Could not create an EpisodeFile for {}".format(self))
        
    def _process(self):
        if not self.filename: return
        basename, self.extension = os.path.splitext(os.path.basename(self.filename))
        if self.extension in EpisodeFile.TYPES['episode'] : self.filetype = 'episode'
        elif self.extension in EpisodeFile.TYPES['subtitle'] : self.filetype = 'subtitle'
        else : return False
        m = re.search(r"(.*?)[\.\-_ ]*[Ss]?([\d]{1,2})[Eex](\d\d)[\.\-_ ]*(.*)",basename)
        if not m: return False
        self.series,self.season,self.number,self.version = [re.sub(r"[\.\- ]","_",x).lower() for x in m.groups()]
        self.season = int(self.season)
        self.number = int(self.number)
        return len(self.series)>0 and self.season>0 and self.number>0

        
    def issubtitle(self): return self.filetype == 'subtitle'
        
    def isepisode(self): return self.filetype == 'episode'
        
    def getfilename(self): return self.filename
        
    def getextension(self): self.extension
        
    def goeswith(self,other):
        #print("Comparing the following files:\n{}\n{}".format(self,other))
        if not isinstance(other, EpisodeFile):
            raise TypeError("Not a EpisodeFile object")
        basic = self.season == other.season \
        and self.number == other.number \
        and difflib.SequenceMatcher(None,self.series,other.series).ratio()>0.5
        if not basic: return 0
        
        if "720p" in self.version or "720p" in other.version:
            if "720p" not in self.version or "720p" not in other.version: return 0

        if "repack" in self.version or "repack" in other.version:
            if "repack" not in self.version or "repack" not in other.version: return 0
        
        versionratio = 1 + difflib.SequenceMatcher(None,self.version,other.version).ratio()
        
        return versionratio
        
    def __str__(self):
        return "{}: Name:<{}> Season <{}> Ep <{}> Version <{}> Ftype <{}>".format(self.filename, self.series,self.season,self.number,self.version,self.filetype)
        
    def __eq__(self,other):
        if not isinstance(other, EpisodeFile):
            raise TypeError("Not a EpisodeFile object")
        print("__eq__ called")
        return self.series == other.series \
        and self.season == other.season \
        and self.number == other.number \
        and self.version == other.version \
        and self.filetype == other.filetype

    def __lt__(self,other):
        if not isinstance(other, EpisodeFile):
            raise TypeError("Not a EpisodeFile object")

        if self.series < other.series: return True
        elif self.series == other.series:
            if self.season < other.season: return True
            elif self.season == other.season:
                if self.number < other.number: return True
                elif self.number == other.number:
                    if self.version < other.version: return True
                    elif self.version == other.version:
                        if self.filetype < other.filetype: return True
        
        return False
        
    def __ne__(self,other): return not self == other
    
    def __le__(self,other): return self == other or self < other     
    
    def __ge__(self,other): return not self < other
    
    def __gt__(self,other): return not self == other and not self < other

class MatchController:
    def __init__(self,directory):
        self.workdir = directory
        if not os.path.exists(directory):
            raise OSError('Could not find {}'.format(directory))
        if not os.path.isdir(directory): 
            raise OSError('{} is not a directory'.format(directory))

        self.episodes = list()
        self.subs = list()
        self.matches = dict()
        
        self.scandirectory()
        
    def scandirectory(self):
        for f in os.listdir(self.workdir):
            try: e = EpisodeFile(os.path.join(self.workdir,f))
            except ValueError: 
                #print(ve)
                continue
        
            if e.isepisode(): self.episodes.append(e)
            elif e.issubtitle(): self.subs.append(e)
            else: print("Unknown file {}".format(f))            

        self.episodes.sort()
        
        for episode in self.episodes:
            filename, _ = os.path.splitext(episode.getfilename())
            match = ''
            bestratio = 0
            for sub in self.subs:
                subratio = episode.goeswith(sub)
                if subratio > 0:
                    if filename != os.path.splitext(sub.getfilename())[0]:
                        #print('Found match ratio {}: {}'.format(subratio,sub.getfilename()))
                        if subratio > bestratio:
                            match = sub.filename
                            bestratio = subratio

                    else:
                        match = None
                        break
            if match is not None: self.matches[episode.filename] = match

    def getmatches(self):
        m = []
        for episode in self.episodes:
            if episode.filename in self.matches :
                m.append((episode.filename,self.matches[episode.filename]))
        return m    

    def newmatch(self,episode,newsub): self.matches[episode]=newsub            
    
    def issubavailable(self,newsub): return newsub not in self.matches.values()
        
    def renamesubs(self,selectedepisodes):
        count = 0
        for episode in selectedepisodes:
            subname = self.matches[episode]
            newname =    os.path.splitext(episode)[0]+os.path.splitext(subname)[1]
            if not subname: continue
            try:
                #print(" >> Renaming {} to {}".format(subname, newname))
                os.rename(subname,newname)
                count +=1
            except Exception as e: print ("Error renaming file {}: {}".format(subname,e))
        return count
