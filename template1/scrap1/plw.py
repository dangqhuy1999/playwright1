import csv
import time
import asyncio
import traceback
from lxml import html
from playwright.async_api import async_playwright, TimeoutError


async def navigate_and_close(page):
    await page.goto('https://www.beinglab-usa.com/lab-equipment/product/86c-ultra-low-temperature-freezer-44', timeout=60000)
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
            full = []
            for one in ones:
                _id_ship = one.get('id')
                if _id_ship != _id_img:
                    continue
                rows = one.xpath(".//tr")
                flag = 0
                
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
            cleaned_data = []
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
            dicton = {}
            for one in ones:
                _id_tab1 = one.get('id')
                if _id_tab1 != _id_img:
                    continue
                datas = one.xpath('.//tr')
                
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
            # process tab4primary <div class="tab-pane fade" id="tab4primary">                 
            tab4primary = tree.xpath("//div[starts-with(@class,'tab-pane fade') and @id='tab4primary']")
            imgs = tab4primary[0].xpath(f'.//span[@class="shubh" and @id="{_id_img}"]/img')
            arr_imgs = f"https://www.beinglab-usa.com{imgs[0].get('src')}"
            print(arr_imgs)
            with open('file.csv',mode='a',newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([f'{_id_img}',f'{hrefs}',f'{full}',f'{cleaned_data}',f'{dicton}',f'{arr}',f'{list_qa}',f'{arr_imgs}'])	
            with open(f'{arr1[i]}.txt','w',encoding = 'utf-8') as file:
                file.write(content)
            i+=1
            
asyncio.run(run())
