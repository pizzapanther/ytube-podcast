import json
import httpx
from bs4 import BeautifulSoup as bs

from feedparser import FeedParserDict

TIMEOUT = 120
HEADERS = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
}

def generate_feed(channel):
  response = httpx.get(f'https://rumble.com/c/{channel}', headers=HEADERS, timeout=TIMEOUT)
  page_soup = bs(response.content, 'html.parser')
  articles = page_soup.find_all("rum-videos-grid")
  articles = articles[0].find_all('script')
  data = json.loads(articles[0].text)
  entries = []
  for item in data['items']:
    link = item['url']
    response = httpx.get(link, headers=HEADERS, timeout=TIMEOUT)
    more_soup = bs(response.content, 'html.parser')
    desc = more_soup.find("p", class_="media-description")
    if desc:
      desc = desc.text.strip()

    else:
      desc = ''

    entries.append(FeedParserDict({
      'title': item['title'],
      'published': item['upload_date'],
      'thumb_url': item['thumb'],
      'link': link,
      'description': desc,
      'summary': desc,
    }))

  return FeedParserDict(
    bozo=False,
    entries=entries,
    feed=FeedParserDict(),
    headers={},
  )
