from machine import UART, Pin
from dfplayer_module import DFPlayer
from number_to_words import number_to_words_list
from time import sleep_ms

# Khai báo các chân UART trên Pico
# Bạn cần nối Pico TX với BT RX, Pico RX với BT TX
BLUETOOTH_UART_ID = 0
BLUETOOTH_TX_PIN = 0
BLUETOOTH_RX_PIN = 1

# Nối Pico TX với DFPlayer RX, Pico RX với DFPlayer TX
DFPLAYER_UART_ID = 1
DFPLAYER_TX_PIN = 4
DFPLAYER_RX_PIN = 5

# Tạo một ánh xạ từ từ khóa tiếng Việt sang số thứ tự file MP3
# Bạn cần đặt tên file MP3 trên thẻ nhớ theo thứ tự từ 001.mp3
WORD_TO_FILE_MAP = {
    "một": 1, "hai": 2, "ba": 3, "bốn": 4, "năm": 5, "sáu": 6, "bảy": 7, "tám": 8, "chín": 9,
    "không": 10, "mười": 11, "trăm": 12, "nghìn": 13, "triệu": 14, "tỷ": 15, "đồng": 16,
    "lẻ": 17, "mươi": 18, "mốt": 19, "tư": 20, "lăm": 21
}

# Khởi tạo UART cho Bluetooth
try:
    bt_uart = UART(BLUETOOTH_UART_ID, baudrate=9600, tx=Pin(BLUETOOTH_TX_PIN), rx=Pin(BLUETOOTH_RX_PIN))
    print("Khởi tạo Bluetooth thành công.")
except Exception as e:
    print(f"Lỗi khởi tạo Bluetooth: {e}")
    
# Khởi tạo DFPlayer
try:
    df_player = DFPlayer(DFPLAYER_UART_ID, DFPLAYER_TX_PIN, DFPLAYER_RX_PIN)
    print("Khởi tạo DFPlayer thành công.")
except Exception as e:
    print(f"Lỗi khởi tạo DFPlayer: {e}")

# Vòng lặp chính để lắng nghe dữ liệu
while True:
    if bt_uart.any():
        try:
            received_data_raw = bt_uart.readline()
            if received_data_raw:
                received_data_str = received_data_raw.decode('utf-8').strip()
                print(f"Dữ liệu nhận được: {received_data_str}")

                # Bắt đầu xử lý dữ liệu ở đây
                parts = received_data_str.split()
                if len(parts) >= 2 and parts[-1] == 'dong':
                    amount_str = parts[-2].replace(',', '') # Loại bỏ dấu phẩy nếu có
                    try:
                        amount = int(amount_str)
                        words_list = number_to_words_list(amount)
                        
                        print(f"Đọc số tiền: {words_list}")
                        
                        for word in words_list:
                            file_number = WORD_TO_FILE_MAP.get(word)
                            if file_number:
                                df_player.play_file(1, file_number)
                                sleep_ms(500)
                            else:
                                print(f"Không tìm thấy file cho từ: {word}")

                    except ValueError:
                        print(f"Không thể chuyển đổi '{amount_str}' thành số.")
                else:
                    print("Dữ liệu không đúng định dạng.")

        except Exception as e:
            print(f"Lỗi khi đọc dữ liệu từ Bluetooth: {e}")
    
    sleep_ms(100)