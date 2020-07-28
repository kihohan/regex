import re
[KB국민카드 1% 청구할인] -> ''
def del_blank_word(text):
    text2 = re.sub(r'\([^)]*\)', '', text)
    text3 = re.sub(r'\[[^\]]*\]', ' ', text2)
    return text3
