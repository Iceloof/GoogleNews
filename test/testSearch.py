import unittest

from GoogleNews import GoogleNews

keyword = 'Apple'

class NumbersTest(unittest.TestCase):

  def testResultNumberWithDefaultPage(self):
    googlenews = GoogleNews()
    googlenews.search(keyword)
    length = len(googlenews.result())
    self.assertEqual(length, 10)
    print('Result length with only one page is correct')

  def testResultNumberWithTwoPages(self):
    googlenews = GoogleNews()
    googlenews.search(keyword)
    googlenews.getpage(2)
    length = len(googlenews.result())
    self.assertEqual(length, 20)
    print('Result length with two pages is correct')

class TestStringMethods(unittest.TestCase):

  def testResultContainsKeyword(self):
    googlenews = GoogleNews()
    googlenews.search(keyword)
    result = googlenews.result()[0]
    self.assertIn(keyword.lower(), result.get('desc').lower())
    print('Result contains keyword')

  def testResultHasLink(self):
    googlenews = GoogleNews()
    googlenews.search(keyword)
    result = googlenews.result()[0]
    self.assertIn('http', result.get('link').lower())
    print('Result contains http link')

  def testResultHasImage(self):
    googlenews = GoogleNews()
    googlenews.search(keyword)
    result = googlenews.result()[0]
    self.assertIn('base64', result.get('img').lower())
    print('Result contains image')

  def testResultHasTitle(self):
    googlenews = GoogleNews()
    googlenews.search(keyword)
    result = googlenews.result()[0]
    self.assertIsNot('', result.get('title').lower())
    print('Result title is not empty')

  def testResultHasMedia(self):
    googlenews = GoogleNews()
    googlenews.search(keyword)
    result = googlenews.result()[0]
    self.assertIsNot('', result.get('media').lower())
    print('Result media is not empty')

  def testResultHasDate(self):
    googlenews = GoogleNews()
    googlenews.search(keyword)
    result = googlenews.result()[0]
    self.assertIsNot('', result.get('date').lower())
    print('Result date is not empty')


if __name__ == '__main__':
  unittest.main()
