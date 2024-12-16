def number_to_words(num):
    if num < 0:
        return "Âm " + number_to_words(-num)
    if num == 0:
        return "Không"

    units = ["", "nghìn", "triệu", "tỷ"]
    digits = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    tens = ["", "", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    words = []

    # Chia số thành từng nhóm ba chữ số
    group_index = 0
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
                    part_words.append("mười")
                else:
                    part_words.append(tens[tens_place] + " mươi")
                    
            if units_place > 0:
                if tens_place == 1:  # Nếu là "mười", không dùng "một"
                    part_words.append(digits[units_place])
                else:
                    part_words.append(digits[units_place])
                    
            part_words.append(units[group_index])
            words.insert(0, " ".join(part_words))
        
        num //= 1000
        group_index += 1

    result =  " ".join(words).strip() + " đồng"
    # Tạo danh sách từ kết quả
    word_map = {
        "một": 1,
        "hai": 2,
        "ba": 3,
        "bốn": 4,
        "năm": 5,
        "sáu": 6,
        "bảy": 7,
        "tám": 8,
        "chín": 9,
        "mười": 10,
        "nghìn": "n",
        "mươi": "m",
        "trăm": "t",
        "triệu": "tt",
        "tỷ": "ttt"
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

    print(result)
except ValueError:
    print("Vui lòng nhập một số nguyên hợp lệ.")