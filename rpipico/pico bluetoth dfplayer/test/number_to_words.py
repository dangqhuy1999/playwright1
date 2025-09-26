def number_to_words_list(num):
    if num == 0:
        return ["khong", "dong"]

    def read_three_digits(n):
        hundreds = n // 100
        tens = (n % 100) // 10
        units = n % 10

        words = []
        if hundreds > 0:
            words.append(digits[hundreds])
            words.append("tram")
        
        if hundreds > 0 and tens == 0 and units > 0:
             words.append("le")
        
        if tens > 1:
            words.append(tens_map[tens])
            if units == 1:
                words.append("mots")
            elif units == 4:
                words.append("tu")
            elif units == 5:
                words.append("lam")
            elif units > 0:
                words.append(digits[units])
        elif tens == 1:
            words.append("muoif")
            if units == 5:
                words.append("lam")
            elif units > 0:
                words.append(digits[units])
        elif units > 0 and hundreds == 0 and tens == 0:
             words.append(digits[units])
        
        return words

    digits = ["", "mot", "hai", "ba", "bon", "nam", "sau", "bay", "tam", "chin"]
    tens_map = ["", "", "hai", "ba", "bon", "nam", "sau", "bay", "tam", "chin"]
    units_map = ["", "nghin", "trieu", "ty"]
    
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

    return result + ["dong"]