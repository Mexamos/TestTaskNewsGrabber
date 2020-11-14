# Test task news grabber

## Description

Grabber articles of news sites:

- http://lenta.ru/rss
- http://www.interfax.ru/rss.asp
- http://www.kommersant.ru/RSS/news.xml
- http://www.m24.ru/rss.xml


## Start project

To run the application you need:

- Install `pyenv` and` pipenv`
- Install Python 3.8 via `pyenv`
- Run `pipenv shell`
- Run `pipenv install`
- Start the application `pipenv run dev`


### Application Functionality

**Getting a list of articles from the selected source:**

```python
graber= Graber()
news = graber.lenta.news(limit=3)
print(news)
```

Output:
```bash
[
  {
    'link': 'https://lenta.ru/news/2020/11/14/abdo/',
    'title': 'Друг Харитонова раскрыл подробности драки с Бородой',
    'desc': '\n    Друг российского бойца смешанного стиля (MMA) Сергея Харитонова Руслан Абдо раскрыл подробности драки спортсмена с Адамом Яндиевым по кличке Борода. «Яндиев вывел нас по одиночке, а не собрал всех вместе и обсудил. Какой-то предмет у него был. Я увидел, что он что-то из рук в руки перекладывает», — рассказал он. \n  ',
    'published': 'Sat, 14 Nov 2020 23:23:00 +0300'
  }
  ...
]
```


**Getting the contents of the article by reference to a specified source:**

```python
url = news[0]['link']
data = graber.lenta.grub(url)
print(data)
```

Output:
```bash
{
  'title': 'Друг Харитонова раскрыл подробности драки с\xa0Бородой',
  'content': [
    'Друг российского бойца смешанного стиля (MMA) Сергея Харитонова Руслан Абдо раскрыл подробности драки спортсмена с Адамом Яндиевым по кличке Борода. Его слова приводит «Спорт-Экспресс».', '«Яндиев вывел нас по одиночке, а не собрал всех вместе и обсудил. Какой-то предмет у него был. Я боковым зрением увидел, что он что-то из рук в руки перекладывает, но не успел рассмотреть, потому что он сразу нанес мне удар», — рассказал Абдо. Он подчеркнул, что на видео заметна реакция Харитинова на удар тяжелым предметом.', 'Драка Харитонова и Яндиева произошла 13 ноября. Отмечалось, что конфликт с Яндиевым произошел после словесной перепалки. Злоумышленник нанес 40-летнему тяжеловесу несколько ударов кастетом, после чего бойца госпитализировали. Позже появилось видео потасовки.', 'Харитонов известен по выступлениям в промоушенах Pride и Bellator. Он одержал 31 победу и потерпел семь поражений.'
  ],
  'image': 'https://icdn.lenta.ru/images/2020/11/14/21/20201114212817865/pic_33c073b994f1bc2928cdd63dafdd3420.jpg'
}
```


**Extending the list of news sites when creating a new instance of the class:**

```python
graber= Graber(additional_data=[
  {
    'name': 'm24',
    'url': 'http://www.m24.ru/rss.xml',
    'article_selectors': {
      'title': 'div.b-material-before-body__data h1', # css selector for find article title in article pages
      'content': 'div.js-mediator-article > p', # css selector for find article content paragraphs in article pages
      'image': 'div.b-material-incut-m-image > img' # css selector for find article image in article pages
    }
  }
])
```
