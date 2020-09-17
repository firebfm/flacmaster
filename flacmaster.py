import re
import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from googletrans import Translator
from shutil import copyfile
import spotsong
import sys

# input qq, spotify or apple url and scrape the tracklist
# then alter the tracklist by simplifying, removing brackets or sanitising illegal characters
# then rename your music

def qqscrape(link):
    req = requests.get(link).content.decode('utf-8')
    
    #.html" title="一个人">一个人</a></span>
    match = re.findall(r'.html\" title=\".*?\">(.*?)</a></span>', req)
    
    #data-stat="data-stat="y_new.album.header.singername" data-mid="002tvW7Q0w3ine" title="彭筝">彭筝</a>
    match2 = re.search(r'data-stat="y_new\.album\.header\.singername" data-mid=".*" title=".*">(.*)</a>', req)
    # match artist names too see if multiple
    match3 = re.search(r'title=".*?">(.*?)</a>', match2.group())
    
    with open("qqtitle.txt", "w", encoding='utf-8') as writefile:
        for track in match:
            writefile.write(track)
            writefile.write('\n')
    
    # if not an album, then custom filename format with artist
    if len(match) <= 4:
        i = 1
        with open("qqfile.txt", "w", encoding='utf-8') as wr:
            for track in match:
                wr.write(str(i).zfill(2) + ". " + match2.group(1) + "() - " +  track + ".flac")
                wr.write('\n')
                i += 1
    
    with open("qqartist.txt", "w", encoding='utf-8') as writefile:
        writefile.write(match2.group(1))
        writefile.write('\n')
        # if more than one artist
        if match2.group(1) != match3.group(1):
            writefile.write(match3.group(1))
            writefile.write('\n')
        
def applescrape(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    divTag = soup.find_all("div", {"class": "song-name typography-label"})
    match = re.findall(r'<!-- -->(.*?)</div>', str(divTag)) 
    with open("apple.txt", "w", encoding='utf-8') as writefile:
        for track in match:
            writefile.write(track.rstrip())
            writefile.write('\n')
        
def changenumb():
    print("Enter path of songs with numbers in filename")
    path = input()
    listflac = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".flac")]
    
    for flac in listflac:
        m = re.search(r'\d', flac)
        newfile = m.group().zfill(2) + Path(flac).name
        os.rename(flac, os.path.join(path, newfile))

# rename auto dir /b and list
def rename():
    print("Enter path of songs to rename using track_new.txt")
    path = input()
    i = 0
    tracktxt = []
    
    with open("track_new.txt", "r", encoding='utf-8') as readfile:
        tracktxt = [line.rstrip() + ".flac" for line in readfile]
    
    listflac = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".flac")]
    
    for flac in listflac:
        #os.rename(flac, tracktxt[i])
        os.rename(flac, path + '\\' + str((i+1)).zfill(2) + '. ' + os.path.basename(tracktxt[i]))
        i += 1

# traditional to simplifed
def trnslte():
    trans = Translator()
    with open('track.txt', 'r', encoding='utf-8') as f:
        contents = f.read()
        result = trans.translate(contents, src='zh-tw', dest='zh-cn')
    with open('track_new.txt', 'w', encoding='utf-8') as f:
        f.write(result.text)
    copyfile('track_new.txt', 'track_simp.txt')

def sanitise_name(name):
    name = re.sub('[\\\/*?"<>|“”]', '', name)
    return re.sub('[:]', ' - ', name)

# for all tracks, remove everything in brackets if > 4 characters
def remove_bracket():
    with open('track_new.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = re.sub(r' *-* \(.{4,}\)', '', line)
            with open('track_new2.txt', 'a', encoding='utf-8') as fi:
                fi.write(line)
    os.remove('track_new.txt')
    os.rename('track_new2.txt','track_new.txt')
    
while True: 
    print("Enter qq or apple or spotify url, 1 changenum format, 2 simplify chn, 3 remove bracket and sanitise, 4 rename")
    mynum = input()
    if 'y.qq.com' in mynum:
        qqscrape(mynum)
        print("success")
    elif 'music.apple.com' in mynum:
        applescrape(mynum)
        print("success")
    elif 'open.spotify.com' in mynum:
        spotsong.spot_album_tracks(mynum)
        print("success")
    elif mynum == '1':
        changenumb()
    elif mynum == '2':
        trnslte()
    elif mynum == '3':
        remove_bracket()
        with open("track_new.txt", "r", encoding='utf-8') as f:
            contents = f.read()
            san_contents = sanitise_name(contents)
        with open('track_new.txt', 'w', encoding='utf-8') as f:
            f.write(san_contents)
    elif mynum == '4':
        rename()
        break;
    elif mynum == '-1':
        break;
