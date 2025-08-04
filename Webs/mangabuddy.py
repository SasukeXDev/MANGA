from .scraper import Scraper
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, quote_plus
import re
import json

class MangaBuddyWebs(Scraper):
  def __init__(self):
    super().__init__()
    self.url = "https://mangabuddy.com/"
    self.bg = True
    self.sf = "mb"
    self.headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
    }

  async def search(self, query: str = "", page: int = 1):
    search_url = f"{self.url}search?{quote_plus(query)}"
    content = await self.get(search_url, headers=self.headers)

    bs = BeautifulSoup(content, "html.parser")
    cards = bs.find_all("div", {"class": "book-item"})

    results = []
    for card in cards:
      data = {}
      anchor = card.a
      if not anchor:
        continue

      data['title'] = anchor.get("title").strip()
      data['url'] = urljoin(self.url, anchor.get('href').strip())
      data['poster'] = anchor.find("img").get('data-src').strip()
      data['id'] = data['url'].split("/")[-1]
      data['api_url'] = f'{self.url}api/manga{anchor.get("href").strip()}/chapters?source=detail'
      results.append(data)

    return results[(page - 1) * 20:page * 20] if page != 1 else results

  async def get_chapters(self, data, page: int = 1):
    content = await self.get(data['url'], headers=self.headers)
    if content:
      bs = BeautifulSoup(content, "html.parser")
      
      des = bs.find("div", class_="summary-content")
      des = des.text.strip() if des else "N/A"

      genres = bs.find("div", class_="genres-content")
      gen = " ".join(g.text.strip() for g in genres.find_all("a")) if genres else "N/A"

      data['msg'] = f"<b>{data['title']}</b>\n\n"
      data['msg'] += f"<b>Genres:</b> <blockquote expandable><code>{gen}</code></blockquote>\n\n"
      data['msg'] += f"<b>Description:</b> <blockquote expandable><code>{des}</code></blockquote>\n"

      container = bs.find('ul', {'id': 'chapter-list'})
      data['chapters'] = container

    return data

  def iter_chapters(self, data, page: int = 1):
    chapters = []
    items = data['chapters'].find_all('li') if data.get('chapters') else []

    for li in items:
      a_tag = li.find('a')
      if not a_tag:
        continue

      title = a_tag.find('strong', {'class': 'chapter-title'}).text.strip()
      url = urljoin(self.url, a_tag.get('href').strip())

      chapters.append({
        "title": title,
        "url": url,
        "manga_title": data['title'],
        "poster": data['poster']
      })

    return chapters[(page - 1) * 20:page * 20] if page != 1 else chapters

  async def get_pictures(self, url, data=None):
    content = await self.get(url, headers=self.headers)
    regex = rb"var chapImages = '(.*)'"
    try:
      imgs = re.findall(regex, content)[0].decode().split(',')
      return imgs
    except IndexError:
      return []

  async def get_updates(self, page: int = 1):
    content = await self.get(f"{self.url}home-page", headers=self.headers)
    bs = BeautifulSoup(content, "html.parser")
    container = bs.find('div', {'class': 'container__left'})
    manga_items = container.find_all('div', {'class': 'book-item'}) if container else []

    updates = []

    for item in manga_items:
      try:
        manga_a = item.find('a')
        if not manga_a:
          continue

        manga_href = manga_a.get('href')
        manga_url = f"{self.url}api/manga{manga_href}/chapters?source=detail"

        chapter_item = item.find("div", {"class": "chap-item"})
        if not chapter_item or not chapter_item.a:
          continue

        chapter_url = urljoin(self.url, chapter_item.a.get('href'))

        updates.append({
          "url": urljoin(self.url, manga_href),
          "api_url": manga_url,
          "chapter_url": chapter_url,
          "manga_title": manga_a.get("title", "").strip(),
          "title": chapter_url.split("/")[-1]
        })
      except Exception as e:
        continue

    return updates
