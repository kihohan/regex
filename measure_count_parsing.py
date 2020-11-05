'''
    EC 특화 패턴들의 정의.
'''
import re

# symbols = '[\[\]\(\)\{\}/_,\-~]'
# measure = '(\d+\.?\d*)\s*(ml|oz|온스|l|m|g|%)'
# bundle = '(\d+)\s*(pack|box|ea|개입|e|p|포|종|팩|개|장|입)'
# digits = '\d+'
# pattern_spf = 'spf \d+ [\+]*'.replace(' ', '\s*')
# pattern_pa = 'pa [\+]+'.replace(' ', '\s*')
# um = 'fl\. oz|리터|ml|kg|oz|l|g|k'
#uc = '박스|번들|개입|개씩|매씩|세트|set|pcs|ea|캔|봉|장|매|개|입|병|포|팩|통|p'

maker_brand = [
    ('에이블C&C', '미샤'),
    ('스타일난다', '3CE'),
    ('크리스찬디올', '크리스찬디올'),
    ('카버코리아', '에이에이치씨'),
    ('클리오', '클리오'),
    ('에스티로더', '에스티로더'), # 1, 2

    ('LG생활건강', '더후'), # 1, 2, 3
    ('LG생활건강', '빌리프'), # 1, 2, 3
    ('LG생활건강', '숨37도'), # 1, 2, 3

    ('아모레퍼시픽', '라네즈'), # 1, 2, 3
    ('아모레퍼시픽', '아이오페'), # 1, 2
    ('아모레퍼시픽', '한율'), # 1, 2
    ('아모레퍼시픽', '헤라'), # 1, 2, 3
    ('아모레퍼시픽', '프리메라'), # 1, 2
    ('아모레퍼시픽', '설화수'),
    ('아모레퍼시픽', '마몽드'),
]


dm = '\d+\.\d+|\d+'
um = 'oz\.?|g(?![a-z])|ml|kg'
dc = '\d+'
uc = '박스|개입|set|pcs|ea|개|입|병|팩|통|p'

base_std = [
    # target <== pattern
    (' $$SPF$$ ', 'spf \d+ [\+]*'),
    (' $$PA$$ ', 'pa [\+]+'),
    (' ', '\s+'),
]

patterns_preprocess = [
    # '_' --> ''
    {
        'pat' : f'(^_$)',
        'key' : ('under_score'),
        'rep' : [''],
    },

    # 기획 세트 22년 8월까지 최신 -> 기획 세트 최신
    {
        'pat' : f'(\d+) (연|년) (\d+) 월 까지?',
        'key' : ( 'y', 'uy', 'm' ),
        'rep' : [ '' ],
    },

    # 기타 연도 월 일 등 날짜 표현
    {
        'pat' : f'(\d+) (연|년)',
        'key' : ( 'y', 'uy' ),
        'rep' : [ '' ],
    },
    {
        'pat' : f'(\d+) 월',
        'key' : ( 'm', ),
        'rep' : [ '' ],
    },
    {
        'pat' : f'(\d+) 일',
        'key' : ( 'd', ),
        'rep' : [ '' ],
    },


    # 15%+15%쿠폰
    {
        'pat' : f'(\d+) % \+ (\d+) %',
        'key' : ( 'p1', 'p2' ),
        'rep' : [ '' ],
    },

    # +15%
    {
        'pat' : f'\+ (\d+) %',
        'key' : ( 'p', ),
        'rep' : [ '' ],
    },

    # ~upto 50%
    {
        'pat' : f'(\d+) %',
        'key' : ( 'p', ),
        'rep' : [ '' ],
    },

    # 에멀젼 120ml (5150679) -> 에멀젼 120ml
    {
        'pat' : f'\( (\d+) \)',
        'key' : ( 'no', ),
        'rep' : [ '' ],
    },


    # _1.1g --> 1.1g
    {
        'pat' : f'_ ({dm}) ({um})',
        'key' : ('dm', 'um'),
        'rep' : [' ', 'dm', 'um'],
    },

    # _1개 -> 1개
    {
        'pat' : f'_ ({dc}) ({uc})',
        'key' : ('dc', 'uc'),
        'rep' : [' x', 'dc', 'uc'],
    },


    # 숨37도(401~)_433 -> 숨37도(401~) 433 : "_ 숫자 단위" 형태처리 뒤에 위치해야 함
    {
        'pat' : f'_(\d+)',
        'key' : ( 'no', ),
        'rep' : [ ' ' ],
    },

    # 27_빌리프 -> 빌리프
    {
        'pat' : f'(\d+)_',
        'key' : ( 'no', ),
        'rep' : [ '' ],
    },

    # 2g/0.066oz --> 2g
    {
        'pat' : f'({dm}) ml / ({dm}) oz\.?',
        'key' : ('dm', 'dm_aux'),
        'rep' : ['dm', 'ml'],
    },

    # 1.1g (0.03oz.) --> 1.1g
    {
        'pat' : f'({dm}) ({um}) \( ({dm}) ({um}) \)',
        'key' : ('dm', 'um', 'dm_aux', 'um_aux'),
        'rep' : ['dm', 'um'],
    },

    # 22g 1+1+1 --> 22g x3
    {
        'pat' : f'({dm}) ({um}) 1 \+ 1 \+ 1',
        'key' : ('dm', 'um'),
        'rep' : ['dm', 'um', ' x3 '],
    },

    # 150ml 1+1 --> 150ml x2
    {
        'pat' : f'({dm}) ({um}) 1 \+ 1',
        'key' : ('dm', 'um'),
        'rep' : ['dm', 'um', ' x2 '],
    },

    #  50ml + 10ml x 5p ==> (50 add (10 x 5))ml  --- "250ml+150ml --> (250 add 150)ml" 이 패턴보다는 앞에 둬라
    {
        'pat' : f'({dm}) ({um}) \+ ({dm}) ({um}) x ({dc}) ({uc})',
        'key' : ('dm', 'um', 'dm_add', 'um_add', 'dc', 'uc'),
        'rep' : ['(', 'dm', ' add ', '(', 'dm_add', ' x ', 'dc', ')', ')', 'um'],
    },

    # 250ml+150ml --> (250 add 150)ml
    {
        'pat' : f'({dm}) ({um}) \+ ({dm}) ({um})',
        'key' : ('dm', 'um', 'dm_add', 'um_add'),
        'rep' : ['(', 'dm', ' add ', 'dm_add', ')', 'um'],
    },

    # .... 1+1
    {
        'pat' : f'(1 \+ 1)$',
        'key' : ('1_1', ),
        'rep' : [' x2'],
    },

    # 1+1 ... 7g x 2 --> 7g x2
    {
        'pat' : f'1 \+ 1 (.* ({dm}) ({um}) x 2)',
        'key' : ('new', 'dm_last_digit_only', 'um'),
        'rep' : ['new'],
    },

    # 1+1 ... 150ml --> 150ml x2
    {
        'pat' : f'1 \+ 1 (.* ({dm}) ({um}))',
        'key' : ('new', 'dm_last_digit_only', 'um'),
        'rep' : ['new', ' x2 '],
    }
]




# pattern을 최대한 simple하게 하여서 나열하자.
# list의 순서는 match하게될 순서임 (중요)
patterns_measure = [
    # (50 add (10 x 5))ml
    {
        'pat' : f'\( ({dm}) add \( ({dc}) x ({dc}) \) \) ({um})', # 이러한 패턴을 검색하면
        'key'  : ('dm', 'dc', 'dp', 'um') # 이러한 matching group이 생성된다
    },

    # (250 plus 150)ml
    {
        'pat' : f'\( ({dm}) add ({dm}) \) ({um})', # 이러한 패턴을 검색하면
        'key'  : ('dm', 'dm', 'um') # 이러한 matching group이 생성된다
    },


    # 200g x 48개(1박스)
    {
        'pat' : f'({dm}) ({um}) [*×xⅹ] ({dc}) ({uc}) \( ({dc}) ({uc}) \)', # 이러한 패턴을 검색하면
        'key'  : ('dm', 'um', 'dp', 'up', 'dc', 'uc') # 이러한 matching group이 생성된다
    },

    # 200g x 48개 1박스
    {
        'pat' : f'({dm}) ({um}) [*×xⅹ] ({dc}) ({uc}) ({dc}) ({uc})', # 이러한 패턴을 검색하면
        'key'  : ('dm', 'um', 'dp', 'up', 'dc', 'uc') # 이러한 matching group이 생성된다
    },

    # (500gx2개)x2세트
    {
        'pat' : f'({dm}) ({um}) [*×xⅹ] ({dc}) ({uc})? \) [*×xⅹ] ({dc}) ({uc})?', # 이러한 패턴을 검색하면
        'key'  : ('dm', 'um', 'dp', 'up', 'dc', 'uc') # 이러한 matching group이 생성된다
    },

    # 130g × 3개입 x 4개
    {
        'pat' : f'({dm}) ({um}) [*×xⅹ]? ({dc}) ({uc}) [*×xⅹ]? ({dc}) ({uc})', # 이러한 패턴을 검색하면
        'key'  : ('dm', 'um', 'dp', 'up', 'dc', 'uc') # 이러한 matching group이 생성된다
    },
    # 1kg씩x4종, 290gPET용기x1개, 1.2kgPETx1개
    {
        #'pat' : f'({dm}) ({um}) 씩|pet|pet용기 [*×xⅹ] ({dc}) ({uc})?',
        'pat' : f'({dm}) ({um}) (씩|pet|pet용기) [*×xⅹ] ({dc}) ({uc})?',
        'key'  : ('dm', 'um', '_', 'dc', 'uc')
    },

    # 1kg(파우치)x2
    {
        'pat' : f'({dm}) ({um})? \(.+\) [*×xⅹ] ({dc}) ({uc})?',
        'key'  : ('dm', 'um', 'dc', 'uc')
    },

    # 195g x 3, 195g x 3개
    {
        'pat' : f'({dm}) ({um}) [*×xⅹ] ({dc}) ({uc})?',
        'key'  : ('dm', 'um', 'dc', 'uc')
    },
    # 500g (4개)
    {
        'pat' : f'({dm}) ({um}) \( ({dc}) ({uc}) \)',
        'key'  : ('dm', 'um', 'dc', 'uc')
    },
    # 195g x 3개, 195g 3개
    {
        'pat' : f'({dm}) ({um}) [*×xⅹ]? ({dc}) ({uc})',
        'key'  : ('dm', 'um', 'dc', 'uc')
    },
    # 195g
    {
        'pat' : f'({dm}) ({um})',
        'key'  : ('dm', 'um')
    },
    # 2개
    {
        'pat' : f'({dc}) ({uc})',
        'key'  : ('dc', 'uc')
    },
    # x2
    {
        'pat' : f'[*×xⅹ] ({dc})',
        'key'  : ('dc', )
    },
]

patterns_preprocess = [{'pat':p['pat'].replace(' ', '\s*'), 'key' : p['key'], 'rep':p['rep']} for p in patterns_preprocess]
patterns_measure = [{'pat' : p['pat'].replace(' ', '\s*'), 'key' : p['key']} for p in patterns_measure]

def set_debug_stat(debug_stat):
    global DEBUG
    DEBUG = debug_stat

def measure_count_parsing(s, direction='forward'):
    mo_list = []
    for p in patterns_measure:
        pat = p['pat']
        key = p['key']

        found = re.search(pat, s) # 해당 pattern으로 찾아진 첫번째 match를 저장

        if not found: # 해당 pattern에 match가 없으면 다음 pattern으로
            continue

        mo_list.append((found, key)) # match, key pair 저정
        s = s[found.span()[1]:] # 다음 match가 시작될 부분 지정

    if len(mo_list) == 0: # 어떤 패턴도 없다
        return '', '', '', '', '', ''
        #return None, None, None, None, None, None

    mo_list = mo_list if direction == 'forward' else reversed(mo_list)

    for mo, key in mo_list:
        val = mo.groups()
        #print(val)
        #print(key)

        dm_val = 0
        dp_val = ''
        dc_val = ''
        um_val = ''
        up_val = ''
        uc_val = ''

        match = {}
        for k, v in zip(key, val):
            #print(k, v)

            # 동일 key에 binding된 digits은 더하자.
            if k.startswith('dm'):
                dm_val = dm_val + (float(v) if '.' in v else int(v))
            if k.startswith('dp'):
                dp_val = int(v) if dp_val == '' else dp_val + int(v)
            if k.startswith('dc'):
                dc_val = int(v) if dc_val == '' else dc_val + int(v)

            # unit이 여러개가 나오는 경우는 무시하자
            if k.startswith('um'):
                um_val = v
            if k.startswith('uc'):
                uc_val = v
            if k.startswith('up'):
                up_val = v

        match = {k : v for k, v in zip(['dm', 'um', 'dp', 'up', 'dc', 'uc'], [str(dm_val) if dm_val != 0 else '', um_val, str(dp_val), up_val, str(dc_val), uc_val])}

        if match.get('dm', None) == match.get('dp', None) == match.get('dc', None) == None: # 숫자는 없이 단위부분만 우연히 matching된 경우는 다음 match로
            continue

        dm_, um_, dp_, up_, dc_, uc_ = match.get('dm', None), match.get('um', None), match.get('dp', None), match.get('up', None), match.get('dc', None), match.get('uc', None)

        #return '' if dm_ == None or '0' else dm_, '' if um_ == None or '0' else um_, '' if dp_ == None or '0' else dp_, '' if up_ == None or '0' else up_, '' if dc_ == None or '0' else dc_, '' if uc_ == None or '0' else uc_
        return '' if dm_ == None else dm_, '' if um_ == None else um_, '' if dp_ == None else dp_, '' if up_ == None else up_, '' if dc_ == None else dc_, '' if uc_ == None else uc_

    return '', '', '', '', '', ''

if __name__ == "__main__":
    pass
    '''
    pattern_list = ['미샤 (250 add 150)ml', '아이브로우x2개']
    for i in pattern_list:
        print (i, '->', measure_count_parsing(i))
    미샤 (250 add 150)ml -> ('400', 'ml', '', '', '', '')
    아이브로우x2개 -> ('', '', '', '', '2', '개')
    '''
