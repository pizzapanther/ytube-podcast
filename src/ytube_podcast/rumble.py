import httpx
from bs4 import BeautifulSoup as bs

from feedparser import FeedParserDict

TIMEOUT = 120
HEADERS = {
  "User-Agent": "Mozilla/5.0 (iPhone; CPU OS 26_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Mobile/14E304 Safari/605.1.15"
}

def generate_feed(channel):
  response = httpx.get(f'https://rumble.com/c/{channel}', headers=HEADERS, timeout=TIMEOUT)
  page_soup = bs(response.content, 'html.parser')
  articles = page_soup.find_all("div", class_="videostream")
  entries = []
  for article in articles:
    if article.find('time') is None:
      continue

    link = f'https://rumble.com{article.find('a')['href']}'
    response = httpx.get(link, headers=HEADERS, timeout=TIMEOUT)
    more_soup = bs(response.content, 'html.parser')
    desc = more_soup.find("p", class_="media-description")
    if desc:
      desc = desc.text.strip()

    else:
      desc = ''

    entries.append(FeedParserDict({
      'title': article.find('h3').text.strip(),
      'published': article.find('time')['datetime'],
      'thumb_url': article.find('img')['src'],
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
