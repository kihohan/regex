import re
from itertools import repeat
from collections import OrderedDict
# ams_return('디올/샤넬/랑방 립스틱 판매합니다','디올|샤넬') -> ['디올', '샤넬']
def ams_return(text,regex):
    del_space = re.sub(re.compile(r'\s+'), '',text)
    cleanText = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', del_space)
    p = re.compile(regex).findall(cleanText)
    return list(OrderedDict(zip(p, repeat(None))))
