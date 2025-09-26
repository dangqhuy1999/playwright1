from utime import sleep_ms, sleep
from picodfplayer import DFPlayer
from machine import Pin, UART 
import time
import os

#Constants. Change these if DFPlayer is connected to other pins.
UART_INSTANCE=1
TX_PIN = 4
RX_PIN=5
BUSY_PIN=6
#Create player instance
player=DFPlayer(UART_INSTANCE, TX_PIN, RX_PIN)#, BUSY_PIN)
#Check if player is busy.
#print('Playing?', player.queryBusy())
#Play the first song (001.mp3) from the first folder (01)
#player.playMP3(1)
player.setVolume(27)
# [8,Trieu, 6,5,7,0,10, ty,3, 2,1,muoi,tram,bandanhanduoc, nghin, 4 , 9, dong] 
uart = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13))

def number_to_words(num):
    if num < 0:
        return "Âm " + number_to_words(-num)
    if num == 0:
        return "Không đồng"

    units = ["", "nghìn", "triệu", "tỷ", "nghìn tỷ"]
    digits = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    tens = ["", "mười", "hai mươi", "ba mươi", "bốn mươi", "năm mươi", "sáu mươi", "bảy mươi", "tám mươi", "chín mươi"]

    words = []
    group_index = 0

    # Chia số thành từng nhóm ba chữ số
    while num > 0:
        part = num % 1000
        if part > 0:
            part_words = []
            hundreds = part // 100
            if hundreds > 0:
                part_words.append(digits[hundreds] + " trăm")
            tens_place = (part % 100) // 10
            units_place = part % 10
            
            if tens_place > 0:
                if tens_place == 1 and hundreds > 0:
                    part_words.append("mười")  # "mười" khi có trăm
                else:
                    part_words.append(tens[tens_place])  # "hai mươi", "ba mươi", v.v.
                    
            if units_place > 0:
                part_words.append(digits[units_place])
                
            part_words.append(units[group_index])
            words.insert(0, " ".join(part_words))
        
        num //= 1000
        group_index += 1

    result =  " ".join(words).strip() + " đồng"
    # Tạo danh sách từ kết quả
    word_map = {
        "một": "10",
        "hai": "9",
        "ba": "8",
        "bốn": "15",
        "năm": "3",
        "sáu": "2",
        "bảy": "4",
        "tám": "0",
        "chín": "16",
        "mười": "6",
        "nghìn": "14",
        "mươi": "11",
        "trăm": "12",
        "triệu": "1",
        "tỷ": "7",
        "đồng": "17",
        "0": "5",
        "Bandanhanduoc": "13"
    }

    # Tách kết quả thành danh sách
    result_list = result.split()

    # Thêm các giá trị số vào danh sách
    for i, word in enumerate(result_list):
        if word in word_map:
            result_list[i] = word_map[word]

    return result_list


#In order ror this example-code to work, make sure you have a
#card with at least one folder, containing at least two mp3:s.
#The folders should be named 01, 02 etc and files should be named
#001.mp3, 002.mp3 etc.




# Function to send data
def send_data(data):
    uart.write(data + '\n')


try:
    so_tien = int(input("Nhập một số: "))
    tien = number_to_words(int(so_tien))

    player.playByIndex(14)
    sleep(0.95)
    for i in tien:
        player.playByIndex(int(i)+1)
        sleep(0.22)
except ValueError:
    print("Vui lòng nhập một số nguyên hợp lệ.")
    sleep(3)
    print('Reset play')
    player.reset()

input("wait")

# Main loop
while True:
    result = 'bibi'
    if uart.any():
        received = str(uart.read())
        result = received.split('\\')[0].split('\'')[1]
        print(result)
        if result!='bibi':
          # Send a test message
          send_data("Hello from Pico!")
        if 'tien' in result:
            # Tách chuỗi để lấy số tiền
            so_tien = result.split(': ')[1].split(' ')[0]
            print(f"Số tiền là: {so_tien}")
            try:
                #number = int(input("Nhập một số: "))
                tien = number_to_words(int(so_tien))

                player.playByIndex(14)
                sleep(0.95)
                for i in tien:
                    player.playByIndex(int(i)+1)
                    sleep(0.22)
            except ValueError:
                print("Vui lòng nhập một số nguyên hợp lệ.")
            sleep(3)
            print('Reset play')
            player.reset()
        else:
            print("Chuỗi không chứa 'Số tiền'.")
        print("Received:", result)

        
    time.sleep(2)

