import re
# 1992년 1월 30일에 배송됩니다. -> 에 배송됩니다.
def del_date(text):
    pattern = '(\d+)\s{0,}(연|년)\s{0,}(\d+)월\s{0,}(\d+)일'; repl = ''
    return re.sub(pattern = pattern, repl = repl, string = text)
