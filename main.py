import csv
import time
import asyncio 
from playwright.async_api import async_playwright

async def load_page(url):
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=False, slow_mo=100)
    page = await browser.new_page()
    await page.goto(url)
    
    #processing
    print(await page.content())
    #toi comment ne tui nua ne
    await browser.close()

async def read_urls_from_file(filename):
  urls = []
  with open(filename, 'r', encoding='utf-8') as file:
    for line in file:
      urls.append(line.strip())
  return urls
async def main():
  filename = 'urls.txt'
  urls = await read_urls_from_file(filename)
  print(urls)
  tasks =  [load_page(url) for url in urls]
  await asyncio.gather(*tasks)
    
asyncio.run(main())
