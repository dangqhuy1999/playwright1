def number_to_words_list(num):
    if num == 0:
        return ["không", "đồng"]

    def read_three_digits(n):
        hundreds = n // 100
        tens = (n % 100) // 10
        units = n % 10

        words = []
        if hundreds > 0:
            words.append(digits[hundreds])
            words.append("trăm")
        
        if hundreds > 0 and tens == 0 and units > 0:
             words.append("lẻ")
        
        if tens > 1:
            words.append(tens_map[tens])
            if units == 1:
                words.append("mốt")
            elif units == 4:
                words.append("tư")
            elif units == 5:
                words.append("lăm")
            elif units > 0:
                words.append(digits[units])
        elif tens == 1:
            words.append("mười")
            if units == 5:
                words.append("lăm")
            elif units > 0:
                words.append(digits[units])
        elif units > 0 and hundreds == 0 and tens == 0:
             words.append(digits[units])
        
        return words

    digits = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    tens_map = ["", "", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    units_map = ["", "nghìn", "triệu", "tỷ"]
    
    result = []
    group_index = 0
    num = abs(num)

    while num > 0:
        part = num % 1000
        if part > 0:
            part_words = read_three_digits(part)
            if group_index > 0:
                part_words.append(units_map[group_index])
            result = part_words + result
        num //= 1000
        group_index += 1

    return result + ["đồng"]