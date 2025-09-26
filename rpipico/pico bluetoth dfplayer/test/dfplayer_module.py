from machine import UART, Pin
from time import sleep_ms

class DFPlayer:
    def __init__(self, uart_id, tx_pin_id, rx_pin_id):
        self.uart = UART(uart_id, baudrate=9600, tx=Pin(tx_pin_id), rx=Pin(rx_pin_id))
        self.cmd_buf = bytearray(10)
        self.cmd_buf[0] = 0x7E  # Start byte
        self.cmd_buf[1] = 0xFF  # Version
        self.cmd_buf[2] = 0x06  # Length
        self.cmd_buf[4] = 0x00  # Acknowledge
        self.cmd_buf[9] = 0xEF  # End byte
        sleep_ms(2000)
        self.set_volume(20) # Khởi tạo âm lượng

    def send_cmd(self, cmd, param1=0, param2=0):
        self.cmd_buf[3] = cmd
        self.cmd_buf[5] = param1
        self.cmd_buf[6] = param2
        
        # Checksum
        checksum = 0
        for i in range(1, 7):
            checksum += self.cmd_buf[i]
        checksum = 0 - checksum
        self.cmd_buf[7] = (checksum >> 8) & 0xFF
        self.cmd_buf[8] = checksum & 0xFF

        self.uart.write(self.cmd_buf)
        sleep_ms(100)

    def play_file(self, folder, file):
        self.send_cmd(0x0F, folder, file)

    def set_volume(self, vol):
        self.send_cmd(0x06, 0, vol)
    
    def reset(self):
        self.send_cmd(0x0C, 0, 0)