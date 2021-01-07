import requests
from bs4 import BeautifulSoup
import logging
import re
def getvideos(search_term):
    try:
        url="https://invidious.snopyta.org/search?q="+search_term
        r = requests.get(url, stream=True)
        page = BeautifulSoup(r.content, 'html.parser')
    except Exception as e:
        logging.error(e)
        return
    results=page.find_all(href=re.compile("/watch?"))
    results= results[1::2]
    links=[result.attrs['href'] for result in results]
    titles=[result.text for result in results]
    youtube_link="https://www.youtube.com"+links[0]
    return titles[0],youtube_link;

def getchannel(search_term):
    search_query=search_term+"+channel%3A"
    try:
        url="https://invidious.snopyta.org/search?q="+search_query
        r = requests.get(url, stream=True)
        page = BeautifulSoup(r.content, 'html.parser')
    except Exception as e:
        logging.error(e)
        return
    results=page.find_all(href=re.compile("/channel/"))
    results=[result for result in results if search_term.lower() in result.text.lower()]
    result_url="https://invidious.snopyta.org"+results[0].attrs['href']
    r = requests.get(result_url, stream=True)
    channel = BeautifulSoup(r.content, 'html.parser')
    links=channel.find_all(href=re.compile("/watch?"))
    links = links[1::2]
    video_links=["https://www.youtube.com"+link.attrs['href'] for link in links]
    titles=[link.text for link in links]
    return titles,video_links;
