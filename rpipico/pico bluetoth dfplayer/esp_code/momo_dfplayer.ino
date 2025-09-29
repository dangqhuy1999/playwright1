#include "BluetoothSerial.h"
#include <HardwareSerial.h> // Dùng cho Serial2 trên ESP32
#include <map>
#include <vector>

// --- 2. KHAI BÁO DFPLAYER MINI ---
#define RXD2 16 // ESP32 GPIO 16 (DFPlayer TX)
#define TXD2 17 // ESP32 GPIO 17 (DFPlayer RX)

 

// --- HẰNG SỐ VÀ WORD MAP ---
// Danh sách các từ (dạng C++ char array)
const char* UNITS[] = {"", "nghin", "trieu", "ty", "nghin ty"};
const char* DIGITS[] = {"khong", "mot", "hai", "ba", "bon", "nam", "sau", "bay", "tam", "chin"};
// Lưu ý: tens_prefix phức tạp hơn, ta xử lý logic sau

// Bản đồ từ-mã số file (CHUYỂN ĐỔI CHÍNH XÁC TỪ PYTHON CỦA BẠN)
std::map<String, int> word_map = {
    {"mot", 10}, {"hai", 9}, {"ba", 8}, {"bon", 15}, {"nam", 3},
    {"sau", 2}, {"bay", 4}, {"tam", 17}, {"chin", 16},
    {"khong", 6},
    {"muoif", 5}, {"tram", 11}, {"nghin", 14}, {"trieu", 12}, {"ty", 1},
    {"dong", 7},
    {"le", 19}, {"muoi", 13}, {"mots", 18}, {"lam", 20},
    {"Bandanhanduoc", 21}
};

// Hàm khai báo
std::vector<int> number_to_file_codes(long num); 
std::vector<int> read_group_of_three(int part);

// --- 1. KHAI BÁO BLUETOOTH SERIAL ---
BluetoothSerial SerialBT;
String receivedData = "";


// Chân BUSY (nếu có thể, nên dùng để kiểm tra trạng thái phát)
// const int BUSY_PIN = 6; 
// Đặt tên cho cổng UART thứ 2
HardwareSerial SerialDFPlayer(2); 

// --- 3. KHAI BÁO CÁC HÀM DFPLAYER CỦA BẠN ---
void sendDFCommand(byte Command, int ParData);
void changeVolume(int thevolume);
void playTrack(int tracknum);
void volumeUp();
void volumeDown();
void playNext();

// Hàm chuyển đổi số sang mã file âm thanh (Chuyển đổi logic MicroPython sang C++)
// Giữ nguyên logic map mã số của bạn: 21 là "Bạn đã nhận được", 7 là "đồng"...
std::vector<int> number_to_file_codes(long num); 
/*
void wait_for_dfplayer_finish() {
    delay(50); // Chờ DFPlayer bắt đầu phát
    // Chờ cho đến khi chân BUSY lên mức HIGH
    while (digitalRead(BUSY_PIN) == LOW) { 
        delay(10); // Tránh tốn CPU
    }
}
*/
// --- SETUP ---
void setup() {

  Serial.begin(115200); // Serial Monitor
  SerialBT.begin("ESP32_BT_VND_Reader"); // Khởi tạo Bluetooth

  // Khởi tạo Serial2 cho DFPlayer
  SerialDFPlayer.begin(9600, SERIAL_8N1, RXD2, TXD2); 
  // pinMode(BUSY_PIN, INPUT_PULLUP); // Khởi tạo chân BUSY
  
  Serial.println("System Initialized: Bluetooth & DFPlayer Ready.");
  delay(3500);
  
  // Cài đặt âm lượng và phát bài test (File 4 của bạn)
  changeVolume(12); 
  delay(100);
  // playTrack(4); // Test
}

// --- LOOP ---
// Giả sử chuỗi đến là: "So tien: 1200 Đ da duoc chuyen vao tai khoan cua ban"

void loop() {
    // --- A. NHẬN VÀ XỬ LÝ LỆNH TỪ BLUETOOTH ---
    while (SerialBT.available()) {
        char incomingChar = SerialBT.read();
        receivedData += incomingChar; 

        if (incomingChar == '\n') { // Khi nhận đủ 1 dòng (lệnh)
            receivedData.trim();
            Serial.print("Received BT: ");
            Serial.println(receivedData);

            // Kiểm tra: Chuỗi chứa "tien:" hoặc "So tien:"
            int keywordPos = receivedData.indexOf("tien:");
            
            if (keywordPos != -1) { 
                // Tách: Tìm số tiền bắt đầu ngay sau "tien:"
                int startPos = keywordPos + String("tien:").length();
                String tempStr = receivedData.substring(startPos);
                tempStr.trim();
                
                // Tách tiếp: Lấy số tiền cho đến khi gặp khoảng trắng đầu tiên
                int endPos = tempStr.indexOf(' '); 
                if (endPos == -1) {
                    endPos = tempStr.length(); // Nếu không có khoảng trắng (chỉ có số)
                }
                
                String numStr = tempStr.substring(0, endPos);
                long so_tien = numStr.toInt(); 
                
                // --- XỬ LÝ LOGIC DFPLAYER ---
                if (so_tien > 0) {
                    Serial.println("Đang phát âm thanh...");
                    
                    std::vector<int> tien_codes = number_to_file_codes(so_tien);
                    
                    playTrack(21); // Bandanhanduoc
                    //wait_for_dfplayer_finish(); // Đợi cho đến khi file âm thanh phát xong
                    delay(1400); 
                    
                    for (int code : tien_codes) {
                        playTrack(code);
                        //wait_for_dfplayer_finish(); // Đợi cho đến khi file âm thanh phát xong
                        delay(1700); 
                    }
                    
                    playTrack(7); // dong
                    //wait_for_dfplayer_finish(); // Đợi cho đến khi file âm thanh phát xong
                    delay(1500);
                    
                    SerialBT.println("Phát âm thanh thành công."); 
                } 
                // Xử lý trường hợp chuỗi hợp lệ nhưng số là 0 hoặc không phải số
                else if (numStr.equals("0")) {
                     SerialBT.println("Số tiền là 0 đồng.");
                }
                else {
                    SerialBT.println("Lỗi: Số tiền không hợp lệ.");
                }
            } else {
                SerialBT.println("Lệnh không hợp lệ. Không tìm thấy 'tien:'.");
            }
            
            receivedData = ""; // Reset buffer
        }
    }

    // --- B. CHUYỂN TIẾP TỪ SERIAL MONITOR QUA BLUETOOTH (Tùy chọn) ---
    if (Serial.available()) {
        SerialBT.write(Serial.read());
    }
}


// Hàm gửi lệnh DFPlayer (Chuyển từ code .ino gốc của bạn)
void sendDFCommand(byte Command, int ParData) {
  byte commandData[10]; //This holds all the command data to be sent
  byte q;
  int checkSum;
  Serial.print("Com: ");
  Serial.print(Command, HEX);
  //Each command value is being sent in Hexadecimal
  commandData[0] = 0x7E;//Start of new command
  commandData[1] = 0xFF;//Version information
  commandData[2] = 0x06;//Data length (not including parity) or the start and version
  commandData[3] = Command;//The command that was sent through
  commandData[4] = 0x00; // Đặt 0x00 để KHÔNG NHẬN phản hồi DFPlayer
  commandData[5] = highByte(ParData);//High byte of the data sent over
  commandData[6] = lowByte(ParData);//low byte of the data sent over
  checkSum = -(commandData[1] + commandData[2] + commandData[3] + commandData[4] + commandData[5] + commandData[6]);
  commandData[7] = highByte(checkSum);//High byte of the checkSum
  commandData[8] = lowByte(checkSum);//low byte of the checkSum
  commandData[9] = 0xEF;//End bit
  SerialDFPlayer.write(commandData, 10);
  delay(100);
}

//play a specific track number
void playTrack(int tracknum){
  Serial.print("Track selected: ");
  Serial.println(tracknum);
  sendDFCommand(0x03, tracknum);
}

//plays the next track
void playNext(){
  Serial.println("Play Next");
  sendDFCommand(0x01, 0);
}

//volume increase by 1
void volumeUp() {
  Serial.println("Vol UP");
  sendDFCommand(0x04, 0);
}
//volume decrease by 1
void volumeDown() {
  Serial.println("Vol Down");
  sendDFCommand(0x05, 0);
}

//set volume to specific value
void changeVolume(int thevolume) {
  sendDFCommand(0x06, thevolume);
}


// Hàm phụ trợ để xử lý 3 chữ số (0-999) và trả về list mã file
std::vector<int> read_group_of_three(int part) {
    std::vector<int> codes;
    if (part == 0) return codes;

    int hundreds = part / 100;
    int tens_place = (part % 100) / 10;
    int units_place = part % 10;
    
    // 1. Hàng trăm
    if (hundreds > 0) {
        codes.push_back(word_map[DIGITS[hundreds]]); // mot, hai, ba...
        codes.push_back(word_map["tram"]); // tram
    }

    // 2. Hàng chục
    if (tens_place == 0) {
        // Xử lý "linh" (le)
        if (hundreds > 0 && units_place > 0) {
            codes.push_back(word_map["le"]); // le (linh)
        }
    } else if (tens_place == 1) {
        // Xử lý "mười" (10-19)
        codes.push_back(word_map["muoif"]); // muoif (mười)
    } else { // tens_place >= 2
        // Xử lý "hai mươi", "ba mươi"...
        // Trong Map của bạn chỉ có các từ đơn, nên ta phải dùng: [DIGITS[tens_place]] + [muoi]
        codes.push_back(word_map[DIGITS[tens_place]]); // hai, ba, bon...
        codes.push_back(word_map["muoi"]); // muoi (file 13)
    }

    // 3. Hàng đơn vị (và các trường hợp đặc biệt: mốt, lăm)
    if (units_place > 0) {
        if (units_place == 1 && tens_place >= 2) {
            // Trường hợp "mốt" (ví dụ: 21)
            codes.push_back(word_map["mots"]);
        } else if (units_place == 5 && tens_place >= 1) {
            // Trường hợp "lăm" (ví dụ: 15, 25)
            codes.push_back(word_map["lam"]);
        } else if (units_place != 0) {
            // Các chữ số còn lại (1, 2, 3, 4, 6, 7, 8, 9)
            // Chỉ thêm nếu không phải trường hợp "lăm" đã xử lý
            if (!(units_place == 5 && tens_place >= 1)) {
                codes.push_back(word_map[DIGITS[units_place]]);
            }
        }
    }

    return codes;
}

// Hàm chính chuyển số sang list mã file
std::vector<int> number_to_file_codes(long num) {
    std::vector<int> final_file_list;
    if (num == 0) {
        // Xử lý 0 đồng: ["khong", "dong"]
        final_file_list.push_back(word_map["khong"]);
        // Mã "dong" (7) đã được thêm ở loop() chính, nên tạm thời không thêm ở đây.
        return final_file_list;
    }
    
    // Xử lý số âm (nếu cần, cần file "am")
    if (num < 0) {
        final_file_list.push_back(word_map["am"]); // Cần thêm "am" vào word_map nếu có file
        num = -num;
    }

    int group_index = 0;
    
    while (num > 0) {
        int part = num % 1000;
        
        if (part > 0) {
            std::vector<int> part_codes = read_group_of_three(part);
            
            // Thêm đơn vị (nghìn, triệu, tỷ)
            if (group_index > 0 && part_codes.size() > 0) {
                // Thêm đơn vị nếu không phải nhóm đơn vị đầu tiên
                final_file_list.insert(final_file_list.begin(), word_map[UNITS[group_index]]);
            }
            
            // Thêm mã số của nhóm 3 chữ số vào đầu list
            final_file_list.insert(final_file_list.begin(), part_codes.begin(), part_codes.end());
        }
        
        num /= 1000;
        group_index++;
    }

    return final_file_list;
}
