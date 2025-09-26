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
player.setVolume(5)
# [8,Trieu, 6,5,7,0,10, ty,3, 2,1,muoi,tram,bandanhanduoc, nghin, 4 , 9, dong] 
uart = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13))

def number_to_words(num):
    if num < 0:
        # Trường hợp số âm: chưa được xử lý đầy đủ trong word_map, cần bổ sung "Âm"
        return ["Âm"] + number_to_words(-num)
    if num == 0:
        # Giả sử "Không đồng" là 2 file: "không" và "đồng"
        return ["không", "đồng"]

    # --- Cập nhật danh sách từ (Thêm các trường hợp đặc biệt) ---
    units = ["", "nghìn", "triệu", "tỷ", "nghìn tỷ"]
    # digits: 0-9
    digits = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    tens_prefix = ["", "mười", "hai mươi", "ba mươi", "bốn mươi", "năm mươi", "sáu mươi", "bảy mươi", "tám mươi", "chín mươi"]

    words = []
    group_index = 0

    while num > 0:
        part = num % 1000
        if part > 0:
            part_words = []
            hundreds = part // 100
            tens_place = (part % 100) // 10
            units_place = part % 10

            # 1. Hàng trăm
            if hundreds > 0:
                part_words.append(digits[hundreds] + " trăm")

            # 2. Hàng chục
            if tens_place == 0:
                # Xử lý "linh" (ví dụ: 105 là "một trăm linh năm")
                if hundreds > 0 and units_place > 0:
                    part_words.append("lẻ")
            elif tens_place == 1:
                # Xử lý "mười" (10-19)
                part_words.append("mười")
            else: # tens_place >= 2
                # Xử lý "hai mươi", "ba mươi",...
                part_words.append(tens_prefix[tens_place])

            # 3. Hàng đơn vị (và các trường hợp đặc biệt: mốt, lăm)
            if units_place > 0:
                if units_place == 1 and tens_place >= 2:
                    # Trường hợp "mốt" (ví dụ: 21 là "hai mươi mốt")
                    part_words.append("mốt")
                elif units_place == 5 and tens_place >= 1:
                    # Trường hợp "lăm" (ví dụ: 15, 25)
                    part_words.append("lăm")
                else:
                    # Các chữ số còn lại (1, 2, 3, 4, 6, 7, 8, 9)
                    # Lưu ý: "năm" không được dùng khi có "mươi" phía trước (đã xử lý bằng "lăm")
                    if not (units_place == 5 and tens_place >= 1):
                        part_words.append(digits[units_place])

            # 4. Đơn vị (nghìn, triệu, tỷ...)
            if part_words:
                part_words.append(units[group_index])
            
            words.insert(0, " ".join(part_words))
        
        num //= 1000
        group_index += 1

    result = " ".join(words).strip() + " đồng"
    
    # --- WORD MAP VÀ MÃ HÓA (Đã được điều chỉnh) ---
    # Tên file phải khớp với số thứ tự, ví dụ: 010 (không), 011 (mười), 012 (trăm)...
    
    # Bổ sung các từ còn thiếu và dùng mã số tương ứng với vị trí file
    # Giả sử số thứ tự các file là:
    # 001-009: Các số 1-9 (được gán trong map thành 1-9)
    # 010: không (được gán là 0)
    # 011: mười (được gán là 10)
    # 012: trăm (được gán là 11)
    
    word_map = {
        # Số 1-9 (Sẽ được cộng 1 ở cuối để ra file 001-009)
        "một": 1, "hai": 2, "ba": 3, "bốn": 4, "năm": 5,
        "sáu": 6, "bảy": 7, "tám": 8, "chín": 9, 
        
        # Các từ khác (Gán trực tiếp mã số file)
        "không": 10,  # File 010.mp3
        "mười": 11,   # File 011.mp3
        "trăm": 12,   # File 012.mp3
        "nghìn": 13,  # File 013.mp3
        "triệu": 14,  # File 014.mp3
        "tỷ": 15,     # File 015.mp3
        "đồng": 16,    # File 016.mp3

        # Các từ đặc biệt mới được thêm vào logic (Cần file mới)
        "linh": 17,    # File 017.mp3
        "mươi": 18,   # File 018.mp3
        "mốt": 19,    # File 019.mp3
        "lăm": 20,    # File 020.mp3
        
        # Các cụm từ và từ bổ sung
        "Bandanhanduoc": 21, # File 021.mp3 (Đổi từ 13 sang 21 để tránh trùng số)
        "Âm": 22, # File 022.mp3
    }

    result_list = result.split()
    final_file_list = []

    for word in result_list:
        if word in word_map:
            code = word_map[word]
            
            # Điều chỉnh logic để tạo tên file 3 chữ số
            if 1 <= code <= 9:
                 # Nếu là số từ 1 đến 9, ta cần dùng file 001.mp3 - 009.mp3
                 file_number = code 
            else:
                 # Các từ khác dùng file 010.mp3 trở đi
                 file_number = code 

            final_file_list.append("{:03d}".format(file_number))
            
    return final_file_list


# Function to send data
def send_data(data):
    uart.write(data + '\n')


player.reset()
for i in range(1,30):
    print(i)
    player.playByIndex(i)
    input("next")
    sleep(0.5)
input("wait")

try:
    so_tien = int(input("Nhập một số: "))
    tien = number_to_words(int(so_tien))
    input(f"Tien: {tien}")
    player.playByIndex(21)
    sleep(0.95)
    for i in tien:
        num = int(i)+1
        input(f"num: {num}")
        player.playByIndex(num)
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

