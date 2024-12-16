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
                if tens_place == 0:  # Nếu không có hàng chục thì thêm "lẻ"
                    part_words.append("lẻ")
                part_words.append(digits[units_place])
                
            part_words.append(units[group_index])
            words.insert(0, " ".join(part_words))
        
        num //= 1000
        group_index += 1

    return " ".join(words).strip() + " đồng"

# Nhập số từ người dùng
try:
    number = int(input("Nhập một số: "))
    result = number_to_words(number)
    print(result)
except ValueError:
    print("Vui lòng nhập một số nguyên hợp lệ.")