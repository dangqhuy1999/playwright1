import time
from playwright.sync_api import sync_playwright
import os

# Tạo thư mục profile nếu chưa tồn tại
profile_dir = 'D:\\IT-Only\\python\\P1\\template1\\my_profile'
os.makedirs(profile_dir, exist_ok=True)

with sync_playwright() as p:
    # Khởi động trình duyệt với context trống
    browser = p.chromium.launch_persistent_context(
        user_data_dir=profile_dir,  # Đường dẫn đến thư mục profile
        headless=False  # Chạy ở chế độ không ẩn
    )

    cookies=input('Do you want clear cookies? Y/N')
    if cookies.lower() == "y":
        # Xóa các cookie và bộ nhớ cache
        browser.clear_cookies()
        browser.clear_permissions()
        browser.set_geolocation({'longitude': 0, 'latitude': 0})  
        print('clear cookies')    

    # Mở một trang mới với User-Agent
    page = browser.new_page()
    page.goto('https://shopee.vn/M%C3%A1y-T%C3%ADnh-Laptop-cat.11035954')
    time.sleep(200)
    # Đóng trình duyệt
    browser.close()