# must use set()
cache = {'write many stopwords'}
def del_stopwords(text):
    return ' '.join([word for word in text.split(' ') if not word in cache])
