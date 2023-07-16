import requests

def checkWebsiteUptime(url: bytes)-> bool:
    try:
        headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
        response = requests.head(url,headers=headers)
        
        response.raise_for_status()

        return True
    except Exception as error:
        print('[helper][webScrapHelper][checkWebsiteUptime][Error] ',error)
        return False


def filterUnreachableWebsites(urlSet: set[bytes])-> list:

    listUrlSet = map(lambda url: url.decode(), list(urlSet))

    return list(filter(lambda url:( checkWebsiteUptime(url) ),listUrlSet))
    

    

    

