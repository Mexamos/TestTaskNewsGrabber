import requests
from bs4 import BeautifulSoup


class Resourse():

  def __init__(self, data):
    self.url = data['url']
    self.name = data['name']
    self.article_selectors = data['article_selectors'] if data.get('article_selectors') else {}
    self.news_data = []

  def loadRSS(self):
    response = requests.get(self.url)

    self.xml_data = response.content

    self.parseXML()

  def parseXML(self):
    soup = BeautifulSoup(self.xml_data, "xml")

    for item in soup.find_all('item'):
      link = item.find('link').get_text()
      title = item.find('title').get_text()
      desc = item.find('description').get_text()
      published = item.find('pubDate').get_text()

      data = {
        'link': link,
        'title': title,
        'desc': desc,
        'published': published
      }

      self.news_data.append(data)

  def news(self, *args, **kwargs):
    if kwargs.get('limit'):
      try:
        return self.news_data[:kwargs.get('limit')]
      except TypeError:
        print('Invalid type of limit')

    return self.news_data

  def grub(self, *args, **kwargs):
    if not args[0]:
      print('Not needed url parametr')
      return

    try:
      response = requests.get(args[0])
    except requests.exceptions.InvalidURL:
      print('Invalid URL')
      return

    soup = BeautifulSoup(response.content, 'html.parser')

    if self.article_selectors.get('title'):
      title = soup.select_one(self.article_selectors['title']).get_text()
    else:
      title = ''

    if self.article_selectors.get('content'):
      content = [paragraph.get_text() for paragraph in soup.select(self.article_selectors['content'])]
    else:
      content = []

    if self.article_selectors.get('image'):
      image = soup.select_one(self.article_selectors['image'])['src']
    else:
      image = ''

    return {
      'title': title,
      'content': content,
      'image': image
    }

class Graber():

  default_data = [
    {
      'name': 'lenta',
      'url': 'http://lenta.ru/rss',
      'article_selectors': {
        'title': 'h1.b-topic__title',
        'content': 'div.b-text > p',
        'image': 'div.b-topic__title-image > img'
      }
    },
    {
      'name': 'interfax',
      'url': 'http://www.interfax.ru/rss.asp',
      'article_selectors': {
        'title': 'article h1[itemprop="headline"]',
        'content': 'article[itemprop="articleBody"] > p',
        'image': ''
      }
    },
    {
      'name': 'kommersant',
      'url': 'http://www.kommersant.ru/RSS/news.xml',
      'article_selectors': {
        'title': 'h1.article_name',
        'content': 'div.article_text_wrapper > p.b-article__text',
        'image': ''
      }
    },
    {
      'name': 'm24',
      'url': 'http://www.m24.ru/rss.xml',
      'article_selectors': {
        'title': 'div.b-material-before-body__data h1',
        'content': 'div.js-mediator-article > p',
        'image': 'div.b-material-incut-m-image > img'
      }
    }
  ]
  resourses_list = []

  def __init__(self, *args, **kwargs):
    self.initResourses(*args, **kwargs)
    self.loadResourseData()

  def initResourses(self, *args, **kwargs):
    if kwargs.get('additional_data') and isinstance(kwargs['additional_data'], list):
      self.default_data = self.default_data + kwargs['additional_data']

    for site in self.default_data:
      resourse = Resourse(site)
      setattr(
        self,
        site['name'],
        resourse
      )
      self.resourses_list.append(resourse)

  def loadResourseData(self):
    for resourse in self.resourses_list:
      resourse.loadRSS()


graber= Graber()
news = graber.lenta.news(limit=3)
print(news)
url = news[0]['link']
data = graber.lenta.grub(url)
print(data)
