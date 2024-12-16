import time
import os

# Hàm để lấy giờ từ người dùng
def set_time():

    #lcd.clear()
    #lcd.print("Set Hour (0-23):")

    hour = int(input())  # Nhập giờ

    #lcd.clear()
    #lcd.print("Set Minute (0-59):")

    minute = int(input())  # Nhập phút

    #lcd.clear()
    #lcd.print("Set Second (0-59):")

    second = int(input())  # Nhập giây
    return hour, minute, second

# Hàm hiển thị thời gian
def display_time(hour, minute, second):
    print(f"{hour:02}:{minute:02}:{second:02}")

# Thiết lập giờ ban đầu
hour, minute, second = set_time()

# Chạy đồng hồ
while True:
    display_time(hour, minute, second)
    time.sleep(1)  # Cập nhật mỗi giây
    os.system('cls')
    second += 1
    if second == 60:
        second = 0
        minute += 1
        if minute == 60:
            minute = 0
            hour += 1
            if hour == 24:
                hour = 0