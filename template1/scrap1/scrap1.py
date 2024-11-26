import json 
import time
import asyncio
import requests
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
#from capmonstercloudclient.requests import RecaptchaV2ProxylessRequest


async def run():
    async with async_playwright() as playwright:
        # Khởi động trình duyệt Chromium
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Điều hướng đến một trang web
        await page.goto('https://example.com')
        print(await page.title())  # In tiêu đề trang

        await browser.close()

# Chạy hàm run
asyncio.run(run())