picogem

Gem tuỳ chỉnh

Sơ đồ nối dây Raspberry Pi Pico với module Bluetooth HC-05 và DFPlayer Mini khá đơn giản. Bạn chỉ cần sử dụng hai cổng UART độc lập trên Pico để giao tiếp với hai module này.



Đây là sơ đồ kết nối chi tiết:



1\. Raspberry Pi Pico và DFPlayer Mini

Bạn sẽ sử dụng UART1 của Pico để giao tiếp với DFPlayer.



Pico (GPIO4) (GP4/UART1 TX) ➞ DFPlayer (RX)



Pico (GPIO5) (GP5/UART1 RX) ➞ DFPlayer (TX)



Pico (GND) (GND) ➞ DFPlayer (GND)



Pico (3V3) (VBUS/3V3 OUT) ➞ DFPlayer (VCC)



2\. Raspberry Pi Pico và Bluetooth HC-05

Bạn sẽ sử dụng UART0 của Pico để giao tiếp với HC-05.



Pico (GPIO0) (GP0/UART0 TX) ➞ HC-05 (RX)



Pico (GPIO1) (GP1/UART0 RX) ➞ HC-05 (TX)



Pico (GND) (GND) ➞ HC-05 (GND)



Pico (3V3) (VBUS/3V3 OUT) ➞ HC-05 (VCC)



3\. DFPlayer Mini và Loa

DFPlayer (SPK1/SPK+) ➞ Loa (+)



DFPlayer (SPK2/SPK-) ➞ Loa (-)



Lưu ý quan trọng

Bạn cần đảm bảo nguồn điện cấp cho Pico đủ mạnh để nuôi cả hai module.



Kiểm tra lại sơ đồ chân trên bo mạch Raspberry Pi Pico của bạn, vì các chân GPIO có thể khác nhau tùy vào phiên bản.



Hãy đảm bảo tốc độ Baud Rate (baudrate) trong code của bạn khớp với tốc độ của các module. Mặc định, cả DFPlayer và HC-05 đều sử dụng 9600.



Bạn có thể muốn tham khảo hình ảnh sơ đồ kết nối trực quan hơn trên các trang web như Wokwi hoặc các diễn đàn công nghệ để có cái nhìn rõ ràng hơn.



Bạn có muốn tôi làm rõ thêm về phần nào trong sơ đồ này không?

