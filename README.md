# GoogleNews

[![Build Status](https://travis-ci.com/HurinHu/GoogleNews.svg)](https://travis-ci.com/HurinHu/GoogleNews)
[![Coverage Status](https://coveralls.io/repos/github/HurinHu/GoogleNews/badge.svg)](https://coveralls.io/github/HurinHu/GoogleNews)
[![PyPI](https://img.shields.io/pypi/v/GoogleNews)](https://pypi.org/project/GoogleNews/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/GoogleNews)](https://pypistats.org/packages/googlenews)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/GoogleNews)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/GoogleNews)
![GitHub contributors](https://img.shields.io/github/contributors/HurinHu/GoogleNews)
![GitHub issues](https://img.shields.io/github/issues-raw/HurinHu/GoogleNews)
![GitHub Action](https://github.com/HurinHu/GoogleNews/workflows/GitHub%20Action/badge.svg)
![GitHub](https://img.shields.io/github/license/HurinHu/GoogleNews)

## Install
```
pip install GoogleNews
```
or
```
pip install --upgrade GoogleNews
```
## Usage
- Initializing
```
from GoogleNews import GoogleNews
googlenews = GoogleNews()
```
- Optional choose language
```
googlenews = GoogleNews(lang='en')
```
- Optional choose period (period and custom day range should not set together)
```
googlenews = GoogleNews(period='d')
```
- Optional choose custom day range (mm/dd/yyyy)
```
googlenews = GoogleNews(start='02/01/2020',end='02/28/2020')
```
- Optional set encode
```
googlenews = GoogleNews(encode='utf-8')
```
or
```
googlenews.setlang('en')
googlenews.setperiod('d')
googlenews.setTimeRange('02/01/2020','02/28/2020')
googlenews.setencode('utf-8')
```
- Search keyword
Default return first page result
```
googlenews.search('APPL')
```
- Get other page of search results
```
googlenews.getpage(2)
```
- Get result
It will return a list, `[{'title': '...', 'media': '...', 'date': '...', 'desc': "...", 'link': '...', 'img': '...'}]`
```
googlenews.result()
```
or just get a list of news titles
```
googlenews.gettext()
```
or just get a list of news links
```
googlenews.getlinks()
```
- Clear result list
Clear result list before you get another search or page
```
googlenews.clear()
```
## Issue
- Image is not working in the latest version, it can only return default google loading gif
