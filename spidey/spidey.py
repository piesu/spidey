#!/usr/bin/python

import urllib2
import re

class spider(object):
  """Klasa crawlujaca strony

  author: Piotr Pies Ostrowski
  """
  pattern_a = re.compile(r'<[aA]([^>]*)>')
  pattern_h = re.compile(r'[hH][rR][eE][fF]=[\'\"]([^\'\"]*)[\'\"]')
  pattern_outside = re.compile(r'(http(|s)://.*)')
  links = []
  visited = []
  links_outside = []
  site = ''
  problems = []

  def a_tags(self, text):
    """Zwraca liste tagow a z danego html'a"""
    return self.pattern_a.findall(text)

  def hrefs(self, text):
    """zwraca adres z tagu a"""
    href = self.pattern_h.findall(text)
    if href :
      return href
    else :
      return ''

  def outside(self, url):
    """zwraca True jezeli link prowadzi na zewnatrz domeny"""
    if self.pattern_outside.findall(url):
      if url.split('/')[2] == site.split('/')[2] :
        return False
      return True
    else:
      return False

  def full_address(self, url):
    """zwraca True jezeli link zawiera przedrostek http://"""
    if self.pattern_outside.findall(url):
      return True
    else:
      return False

  def crawl(self, url):
    """Funkcja crawlujaca konkretny adres"""
    self.links.remove(url)
    self.visited.append(url)
    try:
      sock = urllib2.urlopen(url)
      html = sock.read()
      sock.close()
    except:
      print('Downloading problem - '+url)
      self.problems.append(url)
      return False
    # dziwne, ze to bylo!
    for link in self.a_tags(html):
      if self.hrefs(link) :
        link2 = self.hrefs(link)[0]
        if self.outside(link2):
          if not link2 in self.links_outside :
            self.links_outside.append(link2)
        else :
          if self.full_address(link2) :
            link3 = link2
          else :
            link2 = link2.lstrip('/')
            link3 = str(self.site + '/' + link2)
          if not link3 in self.links and not link3 in self.visited:
            self.links.append(link3)
    return True

  def crawl_site(self, site):
    """funkcja rozpoczynajaca przechodzenie strony"""
    self.site = site.rstrip('/')
    self.links = [site]
    self.run()

  def run(self):
    """glowna petla, kreci sie poki sa strony do obejrzenia"""
    if self.links:
      print(self.links[0])
      self.crawl(self.links[0])
      while len(self.links)>0 :
        print(self.links[0])
        self.crawl(self.links[0])
#      return self.run()
    else :
      return True


if __name__ == '__main__' :
  import sys
  if len(sys.argv) < 2:
      print("Not enough argument's!\nPlease give site address")
      exit()
  site = sys.argv[1]
  proto = site.split('/')[0]
  if not (proto == 'http' or proto == 'https') :
      site = 'http://'+site
  s = spider()
  s.crawl_site(site)
  s.visited.sort()
  for link in s.visited:
    #print link
    pass

  print("\n\nLinks to outside")
  for link in s.links_outside:
    print(link)

