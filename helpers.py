import pickle
import re

from nltk.corpus import stopwords
from pymystem3 import Mystem


def dump_pickle(path, var):
    with open('pickles/' + path, 'wb') as target:
        pickle.dump(var, target)


def load_pickle(path):
    with open('pickles/' + path, 'rb') as target:
        return pickle.load(target)


STOP_WORDS = list(stopwords.words('russian'))
STOP_WORDS.extend(['тасс', 'из\\-за', 'млрд', 'млн', 'тыс', 'руб', 'км'])

RE_BREAKS = re.compile('[\n\r\t]')
RE_SPACES = re.compile(' +')
RE_PUNCTUATION = re.compile('''[–—'"()$€,.%:;/?<>!\\[\\]\\\\+]''')
RE_NUMBERS = re.compile('\\d')
RE_EM_DASH = re.compile(' - ')
RE_STOP_WORDS = re.compile('(\\b' + '\\b|\\b'.join(STOP_WORDS) + '\\b)')

LEMMAS = load_pickle('lemmas')
MYSTEM = Mystem()


def lemma(word):
    lm = LEMMAS.get(word)
    if lm:
        return lm
    mlm = MYSTEM.lemmatize(word)
    LEMMAS[word] = mlm[0]
    return mlm[0]


def lemmatize(row):
    return ' '.join([lemma(word) for word in row.split()])


def trim(row):
    text = row.lower()
    text = RE_BREAKS.sub(' ', text)
    text = RE_BREAKS.sub(' ', text)
    text = RE_SPACES.sub(' ', text)
    text = RE_PUNCTUATION.sub('', text)
    text = RE_NUMBERS.sub(' ', text)
    text = RE_EM_DASH.sub(' ', text)
    return text


def stopwordize(row):
    return RE_STOP_WORDS.sub('', row)


def finalize(row):
    return trim(stopwordize(lemmatize(trim(row))))
