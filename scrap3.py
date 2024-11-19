import time
import asyncio
import traceback
from lxml import html
from playwright.async_api import async_playwright, TimeoutError


async def navigate_and_close(page):
    await page.goto('https://www.beinglab-usa.com/lab-equipment/product/forced-air-drying-oven-19?category=2&t=oven-page', timeout=60000)
    close_button = await page.wait_for_selector('//button[@title="Close"]', timeout=60000)

    await close_button.click()

async def run():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False,slow_mo=500)
        page = await browser.new_page()
        await navigate_and_close(page)
        await page.wait_for_selector('//input[@type="radio"]', timeout=30000)
        
        # Lấy tất cả các radio button
        checks = await page.query_selector_all('//input[@type="radio"]')

        arr1 = []
        for check in checks:
            arr1.append(await check.get_attribute('value'))
        print(arr1)
        i = 0
        for ii in checks:
            await ii.check()
            await page.wait_for_timeout(5000)
            content = await page.content()
            
            #process imageLink
            tree = html.fromstring(content)
            links = tree.xpath("//div[starts-with(@class, 'slick-slide') and not(contains(@class, 'slick-cloned'))]//a")
            _id_img = links[0].get('data-fancybox').split('_')[2]

            hrefs = [f"https://www.beinglab-usa.com{link.get('href')}" for link in links]
            print(f'{_id_img}:\n {hrefs}')
            #process ShippingInfo <div class="tab-pane fade" id="shipping">
            shipping = tree.xpath("//div[starts-with(@class,'tab-pane fade') and @id='shipping']")
            ones = shipping[0].xpath(".//div[@class='shubh']")

            for one in ones:
                _id_ship = one.get('id')
                if _id_ship != _id_img:
                    continue
                rows = one.xpath(".//tr")
                flag = 0
                full = []
                header_omit = []
                for row in rows:
                    headers = row.xpath('.//th')
                    datas = row.xpath('.//td')
                    if headers: 
                        header_1 = headers[0].text.strip() 
                        if datas: 
                            data_1 = datas[0].text.strip()
                            full.append([header_1, data_1])
                        else:
                            header_omit.append(header_1)
                    else:
                        if datas:
                           header_omit.append(datas[0].text.strip()) 
                           if len(header_omit)==3:
                               alter = header_omit.copy()
                               full.append(alter)
                               header_omit.clear()
                print(f'{_id_ship}: {full}')  
            # process tab3primary <div class="tab-pane fade" id="shipping">
            tab3primary = tree.xpath("//div[starts-with(@class,'tab-pane fade') and @id='tab3primary']")
            ones = tab3primary[0].xpath(".//div[@class='shubh']")
            for one in ones:
                _id_tab3 = one.get('id')
                if _id_tab3 != _id_img:
                    continue
                p_tags = one.xpath('.//p')
                arrp = []
                for p in p_tags:
                    arrp.append(' '.join(p.text_content().split()).strip())
                cleaned_data = [item for item in arrp if item]
                print(f'{_id_tab3}: {cleaned_data}')            
            # process tab1primary <div class="tab-pane fade" id="shipping">
            tab1primary = tree.xpath("//div[starts-with(@class,'tab-pane fade') and @id='tab1primary']") 
            ones = tab1primary[0].xpath(".//span[@class='shubh']")
            for one in ones:
                _id_tab1 = one.get('id')
                if _id_tab1 != _id_img:
                    continue
                datas = one.xpath('.//tr')
                dicton = {}
                for data in datas:
                    th_tag = ' '.join(data.xpath('.//th')[0].text_content().split()).strip()
                    td_tags = data.xpath('.//td/p')
                    if len(td_tags)>1:
                        td1 = ' '.join(td_tags[0].text_content().split()).strip()
                        td2 = ' '.join(td_tags[1].text_content().split()).strip()
                        dicton[th_tag] = [td1,td2]
                    else:
                        toyy = ' '.join(td_tags[0].text_content().split()).strip()
                        dicton[th_tag] = [toyy]
                        
                print(f'{_id_tab1}: {dicton}')
            # process documents <div class="tab-pane fade" id="documents">
            documents = tree.xpath("//div[starts-with(@class,'tab-pane fade') and @id='documents']") 
            filenames = documents[0].xpath('.//a[@target="_"]')
            arr = {}
            for filename in filenames:
                link = filename.get('href')
                name = ' '.join(filename[0].text_content().split()).strip()
                arr[link] = [name]
            print(f'{arr}')
            # process faqs <div class="tab-pane fade" id="faqs">
            faqs = tree.xpath("//div[starts-with(@class,'tab-pane fade') and @id='faqs']") 
            questions = faqs[0].xpath('.//div[@class="card-header"]')
            answers = faqs[0].xpath('.//div[@class="collapse"]')
            list_qa = {}
            len_q = len(questions)
            for qa in range (0,len_q):
                key = ' '.join(questions[qa].text_content().split()).strip()
                value = ' '.join(answers[qa].text_content().split()).strip()
                list_qa[key] = value
            print(list_qa)
            with open(f'{arr1[i]}.txt','w',encoding = 'utf-8') as file:
                file.write(content)
            i+=1

asyncio.run(run())

"""
##################################
import traceback
import asyncio
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

start = time.time()
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)  # Khởi động trình duyệt Chromium
    page = browser.new_page()
    page.goto('https://www.beinglab-usa.com/lab-equipment/product/forced-air-drying-oven-19?category=2&t=oven-page',timeout=120000)  # Thay đổi thành URL thực tế
    #https://www.beinglab-usa.com/lab-equipment/product/forced-air-drying-oven-19?category=2&t=oven-page
    new_content = page.content()
    with open('file.txt','w' , encoding='utf-8') as file:
        file.write(new_content)


import asyncio
from pyppeteer import launch

async def download_chromium():
    browser = await launch()
    await browser.close()

asyncio.get_event_loop().run_until_complete(download_chromium())

from requests_html import HTMLSession

# Khởi tạo phiên làm việc
session = HTMLSession()

# Địa chỉ URL bạn muốn gọi
url = 'https://www.beinglab-usa.com/lab-equipment/product/forced-air-drying-oven-19'

fd# Gọi trang web
response = session.get(url)

# Render JavaScript (nếu cần)
response.html.render(executable_path='D:\\IT-Only\\python\\chromedriver.exe')

# Lấy HTML
html_content = response.html.html
with open('file1.txt', 'w' , encoding = 'UTF-8') as file:
	file.write(html_content)



import requests

# Địa chỉ URL bạn muốn gọi
url = 'https://www.beinglab-usa.com/lab-equipment/product/forced-air-drying-oven-19'

# Gọi trang web
response = requests.get(url)

# Kiểm tra trạng thái phản hồi
if response.status_code == 200:
    # Lấy HTML
    html_content = response.text
    print(html_content)
    with open('file1.txt', 'w' , encoding = 'UTF-8') as file:
        file.write(html_content)
else:
    print(f'Error: {response.status_code}')

#######################
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Điều hướng đến trang web
        await page.goto('https://example.com')

        # Đợi cho phần tử xuất hiện (thay 'selector' bằng selector thực tế của bạn)
        element = await page.wait_for_selector('selector')

        # Cuộn đến phần tử
        await page.evaluate('element => element.scrollIntoView()', element)

        # Bạn có thể thực hiện các hành động khác với phần tử sau khi đã cuộn đến
        # Ví dụ: nhấp vào phần tử
        await element.click()

        await browser.close()

# Chạy hàm run
asyncio.run(run())

Để tạo một vòng lặp vô tận cuộn xuống cuối trang trong Playwright, bạn có thể sử dụng một vòng lặp `while` và phương thức cuộn (scroll) để liên tục cuộn xuống cho đến khi không còn thêm nội dung nào nữa. Dưới đây là ví dụ mã Python cho điều này:

### Ví Dụ Mã

```python
import asyncio
from playwright.async_api import async_playwright

async def scroll_to_bottom(page):
    last_height = await page.evaluate("document.body.scrollHeight")

    while True:
        # Cuộn xuống cuối trang
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        
        # Chờ một chút để tải thêm nội dung
        await page.wait_for_timeout(1000)  # Chờ 1 giây

        # Tính chiều cao mới và so sánh với chiều cao cũ
        new_height = await page.evaluate("document.body.scrollHeight")
        if new_height == last_height:
            break  # Nếu không còn nội dung mới thì thoát vòng lặp
        last_height = new_height

async def run():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Điều hướng đến trang web
        await page.goto('https://example.com')  # Thay đổi thành URL thực tế

        # Bắt đầu cuộn xuống
        await scroll_to_bottom(page)

        await browser.close()

# Chạy hàm run
asyncio.run(run())
```

### Giải Thích

1. **`scroll_to_bottom(page)`**: Hàm này thực hiện cuộn xuống cuối trang.
   - **`last_height`**: Lưu chiều cao hiện tại của trang.
   - **Vòng lặp `while True`**: Bắt đầu một vòng lặp vô tận.
   - **Cuộn xuống**: Sử dụng `window.scrollTo(0, document.body.scrollHeight)` để cuộn xuống cuối trang.
   - **Chờ tải nội dung**: Sử dụng `wait_for_timeout(1000)` để chờ một giây cho nội dung mới tải.
   - **Kiểm tra chiều cao mới**: Nếu chiều cao mới không thay đổi so với chiều cao cũ, vòng lặp sẽ dừng lại.

2. **`run()`**: Hàm chính để khởi tạo Playwright và bắt đầu quá trình cuộn xuống.

### Lưu Ý

- **URL thực tế**: Hãy thay thế `'https://example.com'` bằng URL của trang web mà bạn muốn cuộn xuống.
- **Thời gian chờ**: Bạn có thể điều chỉnh thời gian chờ (`1000 ms`) để phù hợp với tốc độ tải của trang web.

### Kết Luận

Bằng cách sử dụng đoạn mã trên, bạn có thể tạo một vòng lặp để cuộn xuống cuối trang cho đến khi không còn nội dung mới để tải. Nếu bạn cần thêm thông tin hoặc có câu hỏi nào khác, hãy cho tôi biết!



Để điền vào ô (input field) và nhấp vào một nút (button) hoặc radio input trong Playwright, bạn có thể sử dụng các phương thức như `fill()` và `click()`. Dưới đây là một ví dụ minh họa bằng Python:

### Ví Dụ Mã

python
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as playwright:
        # Khởi động trình duyệt
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Điều hướng đến trang web
        await page.goto('https://example.com')  # Thay đổi thành URL thực tế

        # Điền vào ô input
        await page.fill('input[name="username"]', 'my_username')  # Thay đổi selector và giá trị cho phù hợp

        # Nhập mật khẩu (nếu cần)
        await page.fill('input[name="password"]', 'my_password')  # Thay đổi selector và giá trị cho phù hợp

        # Nhấp vào nút
        await page.click('button[type="submit"]')  # Thay đổi selector cho nút phù hợp

        # Hoặc nhấp vào radio input
        await page.click('input[type="radio"][value="option1"]')  # Thay đổi selector cho radio button phù hợp

        # Đợi một chút để xem kết quả (tùy chọn)
        await page.wait_for_timeout(2000)

        await browser.close()

# Chạy hàm run
asyncio.run(run())


### Giải Thích Các Bước

1. **Khởi động Playwright**: Khởi động trình duyệt và mở một trang mới.
2. **Điều hướng đến trang web**: Sử dụng `page.goto()` để điều hướng đến URL bạn muốn.
3. **Điền vào ô input**:
   - Sử dụng `page.fill(selector, value)` để điền giá trị vào ô input. Bạn cần thay đổi `selector` cho phù hợp với trường mà bạn muốn điền.
4. **Nhấp vào nút**:
   - Sử dụng `page.click(selector)` để nhấp vào nút. Thay đổi `selector` để phù hợp với nút mà bạn muốn nhấp.
5. **Nhấp vào radio input**:
   - Tương tự, sử dụng `page.click()` để nhấp vào radio button, với selector phù hợp.
6. **Đợi một chút (tùy chọn)**: Sử dụng `wait_for_timeout()` để đợi một thời gian ngắn nếu bạn muốn thấy kết quả trước khi trình duyệt đóng lại.

### Lưu Ý

- **Selector**: Hãy chắc chắn rằng bạn thay đổi các selector trong mã cho phù hợp với các phần tử trên trang mà bạn đang làm việc.
- **Headless**: Nếu bạn muốn chạy trình duyệt mà không hiển thị giao diện, bạn có thể thay đổi `headless=False` thành `True`.

### Kết Luận

Với mã trên, bạn có thể dễ dàng điền vào ô và nhấp vào các phần tử khác nhau trên trang web bằng Playwright. Nếu bạn có thêm câu hỏi hoặc cần thêm thông tin, hãy cho tôi biết!



import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Điều hướng đến trang web
        await page.goto('https://example.com')

        # Đợi cho phần tử xuất hiện (thay 'selector' bằng selector thực tế của bạn)
        element = await page.wait_for_selector('selector')
	# Chờ cho đến khi phần tử xuất hiện
        await page.wait_for_selector('xpath=//input[@name="username"]', timeout=5000)  # Thay đổi timeout nếu cần
        # Cuộn đến phần tử
        await page.evaluate('element => element.scrollIntoView()', element)

        # Bạn có thể thực hiện các hành động khác với phần tử sau khi đã cuộn đến
        # Ví dụ: nhấp vào phần tử
        await element.click()

        await browser.close()

# Chạy hàm run
asyncio.run(run())


import aiohttp
import asyncio
import time

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    urls = ['https://example.com/api' for _ in range(100)]  # Thay thế bằng URL thực tế
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return responses

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    
    print(f'Time taken: {end_time - start_time:.4f} seconds')


import requests

# Địa chỉ URL bạn muốn gọi
url = 'https://www.youtube.com/watch?v=nFn4_nA_yk8&list=PLq29JwxERiRRlBKoNIsVpYgGPMONg4YKw&index='

# Gọi trang web
response = requests.get(url)

# Kiểm tra trạng thái phản hồi
if response.status_code == 200:
    # Lấy HTML
    html_content = response.text
    print(html_content)
    with open('file1.txt', 'w' , encoding = 'UTF-8') as file:
        file.write(html_content)
else:
    print(f'Error: {response.status_code}')


from requests_html import HTMLSession

# Khởi tạo phiên làm việc
session = HTMLSession()

# Địa chỉ URL bạn muốn gọi
url = 'https://www.youtube.com/watch?v=nFn4_nA_yk8&list=PLq29JwxERiRRlBKoNIsVpYgGPMONg4YKw&index=2'

# Gọi trang web
response = session.get(url)

# Render JavaScript (nếu cần)
response.html.render()

# Lấy HTML
html_content = response.html.html
with open('file1.txt', 'w' , encoding = 'UTF-8') as file:
	file.write(html_content)

"""