import re
# del_repeat('abcabc') -> 'abc'
def del_repeat(text):
    s = re.sub(re.compile(r'\s+'), '',text)
    match = re.compile(r"(.+?)\1+$").match(s)
    return match.group(1) if match else s
