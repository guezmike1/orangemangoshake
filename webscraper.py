from lxml import html
import requests
from pprint import pprint


page = requests.get('https://www.oddsshark.com/nba/scores')
tree = html.fromstring(page.content)

print tree
print tree.xpath
#This will create a list of buyers:
buyers = tree.xpath('//div[@class="city"]/text()')
prices = tree.xpath('//div[@class="city"]')
#This will create a list of prices
#prices = tree.xpath('//span[@class="item-price"]/text()')

print 'Buyers: ', buyers
print 'Prices: ', prices
