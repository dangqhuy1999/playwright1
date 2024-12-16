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

# Nhập số từ người dùng
try:
    number = int(input("Nhập một số: "))
    result = number_to_words(number)
    
    print(result)

except ValueError:
    print("Vui lòng nhập một số nguyên hợp lệ.")