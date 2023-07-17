from dataclasses import field
import hashlib
import requests
import xml.etree.ElementTree as ET
import feedparser

MOCK_HEADERS: dict[str:str] = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}


def __check_website_uptime(url: bytes) -> bool:
    try:
        response = requests.head(url, headers=MOCK_HEADERS)
        response.raise_for_status()

        return True

    except Exception:
        return False


def __filter_unreachable_website(url_set: set[bytes]) -> list[str]:
    list_url_set = map(lambda url: url.decode(), list(url_set))
    return list(filter(lambda url: (__check_website_uptime(url)), list_url_set))


def _fetch_feed_live_music_blog(fields) -> dict[str:dict[str:any]]:
    FEED_URL = "https://livemusicblog.com/feed/"
    try:
        feed = feedparser.parse(FEED_URL)
        if not feed["entries"]:
            return

        get_list = fields
        data = feed["entries"]
        high_level_dict = {}

        for i in range(len(data)):
            low_level_dict = {}

            for item in get_list:
                value = data[i][item] if data[i] and data[i][item] else ""
                low_level_dict[item] = value

            uId = hashlib.sha224(low_level_dict["published"].encode(
            )+low_level_dict["title"].encode()).hexdigest()[:5]
            high_level_dict[uId] = low_level_dict

        return feed

    except Exception:
        return None


DATA_SOURCE_MAP_FETCHER: dict[str:dict[str:any]] = {
    "https://livemusicblog.com/feed/": {
        "func": _fetch_feed_live_music_blog,
        "fields": ["title", "author", "published", "tags", "summary"]
    }
}


def load_feeds(url_set: list[bytes]) -> list[dict[str:any]]:
    url_list = list(map(lambda x: x.decode(), url_set))
    if len(url_list) == None:
        return

    final_data = []

    for url in url_list:
        if not DATA_SOURCE_MAP_FETCHER.get(url) or not DATA_SOURCE_MAP_FETCHER.get(url).get("fields") or not DATA_SOURCE_MAP_FETCHER.get(url).get("func"):
            continue

        fields = DATA_SOURCE_MAP_FETCHER[url]["fields"]
        data = DATA_SOURCE_MAP_FETCHER[url]["func"](fields=fields)

        if not data:
            continue

        final_data.append(data)

    return final_data
