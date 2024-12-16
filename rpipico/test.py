import machine
import utime  # Sử dụng utime thay vì time

# Khởi tạo UART
uart = machine.UART(0, baudrate=9600, tx=17, rx=16)  # Thay đổi chân theo cấu hình của bạn

# Gửi lệnh phát bài nhạc 001_music.mp3 trong thư mục 01
command = bytes([0x7E, 0xFF, 0x06, 0x03, 0x01, 0x01, 0x00, 0x7E])
uart.write(command)

# Đợi một chút để DFPlayer xử lý
utime.sleep(5)  # Chờ 5 giây