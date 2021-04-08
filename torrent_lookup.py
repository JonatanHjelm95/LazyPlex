import urllib.request
from pprint import pprint
#from html_table_parser import HTMLTableParser
from bs4 import BeautifulSoup
import lxml
import json

whitelist = ['Trusted', 'VIP']

URL = 'https://thepiratebay10.org/search/'

def lookup(name):
    content = read_contents(name.replace(' ','+'))
    xhtml = content.decode('utf-8')
    soup = BeautifulSoup(xhtml, 'lxml')
    rows = soup.find_all('tr')
    results = []
    for r in rows:
        try:
            result = {}
            result['trusted'] = False
            result['seeders'] = 'x'
            for td in r.find_all('td'):
                if len(td.attrs) == 0 and len(td.contents) > 0:
                    # finding torrent name
                    for div in td.find_all('div'):
                        for a in div.find_all('a'):
                            result['name'] = a.contents[0]
                    for a in td.find_all('a'):
                        # finding magnet
                        if 'magnet' in a.attrs['href']:
                            result['magnet'] = a.attrs['href']
                        # finding trusted
                        for img in a.find_all('img'):
                            try:
                                if whitelisted(img.attrs['title']):
                                    result['trusted'] = True
                            except:
                                continue
                    # finding size
                    try:
                        for font in td.find_all('font'):
                            result['info'] = str(font.contents[0]).replace(', ULed by','')
                    except:
                        continue
                # finding seeders and leechers
                try:
                    if 'right' in td.attrs['align']:
                        if result['seeders'] == 'x':
                            result['seeders'] = td.contents[0]
                        else:
                            result['leechers'] = td.contents[0]
                except:
                    continue
                results.append(result)
        except:
            pass
    if len(results) > 0:
        return results
    else:
        return f'no movies was found with the name: {name}'

def find_torrent_name(div):
    for d in div:
        if len(d.text) > 0:
            return d.text
    return ''


def whitelisted(content):
    return content in whitelist

def read_contents(name):
    #making request to the website
    req = urllib.request.Request(url=f'{URL}{name}')
    f = urllib.request.urlopen(req)
    #reading contents of the website
    return f.read()

if __name__ == '__main__':
    lookup('avengers')