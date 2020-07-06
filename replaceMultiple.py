# replaceMultiple('[Dior] 디오을 어딕트 립 글로우 3.5g', ['Dior','디오을'], '디올') -> '[디올] 디올 어딕트 립 글로우 3.5g'
def replaceMultiple(mainString, toBeReplaces, newString): 
    for elem in toBeReplaces :
        if elem in mainString :
            mainString = mainString.replace(elem, newString)
    return  mainString
