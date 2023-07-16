import hashlib
import requests
import json
import xml.etree.ElementTree as ET
import feedparser
import datetime

mockHeaders: dict[str:str] = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

def __checkWebsiteUptime(url: bytes)-> bool:
    try:

        response = requests.head(url,headers=mockHeaders)
        response.raise_for_status()
        return True
    except Exception as error:
        print('[helper][feedHelper][__checkWebsiteUptime][Error] ',error)
        return False


def __filterUnreachableWebsites(urlSet: set[bytes])-> list[str]:
    listUrlSet = map(lambda url: url.decode(), list(urlSet))
    return list(filter(lambda url:( __checkWebsiteUptime(url) ),listUrlSet))


def _fetchFeedData(url:str)-> dict[str:dict[str:any]]:
    try:
        feed = feedparser.parse(url)
        if not feed["entries"]:
            print("[helper][feedHelper][__fetchFeedData][Error] url",url)
            return

        getList = ["title","author","published","tags","summary"]
        data = feed["entries"]
        highLevelDict = {}
        for i in range(len(data)):
            lowLevelDict = {}
            for item in getList:
                value = data[i][item] if data[i] and data[i][item] else ""
                lowLevelDict[item] = value
                
            uId = hashlib.sha224(lowLevelDict["published"].encode()+lowLevelDict["title"].encode()).hexdigest()[:5]
            highLevelDict[uId] = lowLevelDict
        return feed

    except Exception as error:
        print('[helper][feedHelper][__fetchFeedData][Error] ',error)

def loadFeeds(urlSet: list[bytes]) ->list[dict[str:any]]:
    urlList = list(map(lambda x: x.decode(),urlSet))
    if len(urlList) == None:
        return

    finalData = []

    for url in urlList:
        data = _fetchFeedData(url=url)
        if not data:
            continue
        finalData.append(data)

    return finalData





    

    

    

    

    

    

    

