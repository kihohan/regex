import re
import numpy as np
# ['동원 만두','비비고 만두','중국 딤섬'] - > [['동원F&B'], ['CJ제일제당'], []]
def intergrate_one_word(lst_text):
    dct = [['동원|개성|조이락', '동원F&B'],
            ['비비고|CJ|cj|제일제당|백설|씨제이', 'CJ제일제당']
          ]

    def master_one_word(regex_stc_master, var):
        r = regex_stc_master[0]
        if bool(re.search(r,var)) == True:
            return regex_stc_master[1]
        else:
            return '없음'

    r_1 = []
    for t in lst_text:
        for i in  dct:
            r_1.append(master_one_word(i, t))
    r_2 = [list(x) for x in np.array_split(r_1,len(lst_text))]
    return [[x for x in y if x != '없음'] for y in r_2]
