import re

def find_measure(text, param):
    pattern_price = r'(\d+)\s{0,}(만원|원|만 원)'
    pattern_measure = r'(\d+)\s{0,}(cm|ml|oz|kg|온스|l|m|g|리터)'
    pattern_bundle = r'(\d+)\s{0,}(pack|box|ea|개입|e|p|포|종|팩|개|장|입|만 대)'
    pattern_grade = r'(\d+)\s{0,}(등급|성급|단계)'
    pattern_person = r'(\d+)\s{0,}(명|분)' # 세자리 이상일 경우에만 사람.
    pattern_time = r'(\d+)\s{0,}(시간|시|분|초|월|일|년)'
    
    if param == 'price':
        if re.search(pattern_price, text):
            return 'price'
    elif param == 'measure':
        if re.search(pattern_measure, text):
            return 'measure'
    elif param == 'bundle':
        if re.search(pattern_bundle, text):
            return 'bundle'
    elif param == 'grade':
        if re.search(pattern_grade, text):
            return 'grade'
    elif param == 'person':
        if re.search(pattern_person, text):
            return 'person'
    elif param == 'time':
        if re.search(pattern_time, text):
            return 'time'
          
find_measure('15분 정도면 충분히 다 설치 가능하세요','time')
