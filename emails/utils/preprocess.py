import re
import os
from bs4 import BeautifulSoup
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import spacy
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import pandas as pd
from urllib.parse import urlparse
import re
from tld import get_tld
import os.path

random.seed(123)

MAX_NUM_WORDS = 10000
MAX_SEQUENCE_LENGTH = 1000


# define the lambda functions
def remove_html(body): return BeautifulSoup(
    str(body), 'html.parser').get_text()


def remove_js(body): return re.sub(
    r'<script.*?>.*?</script>', '', body, flags=re.DOTALL)


def preprocess_email(body):
    nlp = spacy.load("en_core_web_sm")
    nlp.max_length = 5862775

    text = remove_js(remove_html(body))
    # Tokenization and lowercasing
    doc = nlp(text.lower())

    # Removal of punctuation and stopwords, stemming and lemmatization
    tokens = []
    for token in doc:
        if token.text not in STOP_WORDS and token.text not in punctuation:
            tokens.append(token.lemma_)

    tokenizer_file = os.path.join(os.path.dirname(
        __file__), 'files', 'email_body_tokenizer.pickle')

    tokenizer = pickle.load(
        open(tokenizer_file, 'rb'))
    numerical_email = tokenizer.texts_to_sequences([" ".join(tokens)])
    padded_email = pad_sequences(numerical_email, maxlen=MAX_SEQUENCE_LENGTH)
    return padded_email


def extract_urls(text):
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = re.findall(url_pattern, text)
    return urls


def detect_cyberbuilling(text):
    print(random.uniform(0.3, 0.5))

    return random.uniform(0.3, 0.5)


def detect_fakenews(text):
    print(random.uniform(0.1, 0.2))
    return random.uniform(0.1, 0.2)


def extract_url_features(url):
    parsed_url = urlparse(url)

    # fct1
    use_of_ip = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        # these are all variations of IPv4
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'
        # IPv4 in hexadecimal
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # all variations of Ipv6

    # fct1
    hostname = urlparse(url).hostname
    hostname = str(hostname)
    abnormal_url = re.search(hostname, url)

    # fct1

    # fct1
    count_dot = url.count('.')

    # fct1
    www_count = url.count('www')

    # fct1
    alt_count = url.count('@')

    # fct1
    urldir = urlparse(url).path
    urldir_count = urldir.count('/')

    # fct1
    urlembed_count = urldir.count('//')

    # fct1
    # verifying the existance of some of the most popular shortenings that can be used by hackers
    shortening_url = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                               'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                               'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                               'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                               'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                               'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                               'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                               'tr\.im|link\.zip\.net',
                               url)
    print(shortening_url)
    # fct1
    count_https = url.count('https')

    # fct
    count_http = url.count('http')

    # number of spaces
    spaces_count = url.count('%')

    # number of ?
    interrogationmark_count = url.count('?')

    # number of hyphens
    hyphen_count = url.count('-')

    # number of equals
    equal_count = url.count('=')

    # url length
    url_length = len(str(url))

    # Hostname Length
    hostname_length = len(urlparse(url).netloc)

    # suspicious words
    suspicious_words = re.search('PayPal|login|signin|bank|account|update|free|lucky|service|bonus|ebayisapi|webscr',
                                 url)

    # number of digits
    digits_count = sum(c.isdigit() for c in url)

    # number of letters
    letters_count = sum(c.isalpha() for c in url)

    # First Directory Length
    urlpath = urlparse(url).path
    fd_length = len(urlpath.split('/')[1]
                    ) if len(urlpath.split('/')) > 1 else 0

    # domain length
    url_data = pd.DataFrame({'url': [url]})
    url_data['domain'] = url_data['url'].apply(
        lambda i: get_tld(i, fail_silently=True) or '')
    tld_length = len(url_data['domain'][0])

    features = {
        'use of IP address': 1 if use_of_ip else 0,
        'abnormal url': 1 if abnormal_url else 0,
        'number of dots': count_dot,
        'number of www':  www_count,
        'number of alts': alt_count,
        'number of directories': urldir_count,
        'number of embeddings in url':  urlembed_count,
        "existance of shortenings": 1 if shortening_url is not None else 0,
        "number of https": count_https,
        "number of http": count_http,
        "number of spaces":  spaces_count,
        "number of interrogation marks":  interrogationmark_count,
        "number of hyphens":  hyphen_count,
        "number of equals":  equal_count,
        "url length":  url_length,
        "hostname lenght":   hostname_length,
        "existance od suspicious words": 1 if suspicious_words is not None else 0,
        "number of digits ":   digits_count,
        "number of letters":   letters_count,
        "first direc length":   fd_length,
        "Length of Top Level Domain": tld_length,



    }
    return list(features.values())
