import pandas as pd
from bs4 import BeautifulSoup
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
import re
import string
from unidecode import unidecode

class DataCleaner:
    def __init__(self):
        self.stop_words = stopwords.words('english')
        self.cList = {
            "i'm": "i am",
            "you're": "you are",
            "it's": "it is",
            "we're": "we are",
            "we'll": "we will",
            "That's":"that is",
            "haven't":"have not",
            "let's":"let us",
            "ain't": "am not / are not / is not / has not / have not",
            "aren't": "are not / am not",
            "can't": "cannot",
            "can't've": "cannot have",
            "'cause": "because",
            "could've": "could have",
            "couldn't": "could not",
            "couldn't've": "could not have",
            "didn't": "did not",
            "doesn't": "does not",
            "don't": "do not",
            "hadn't": "had not",
            "hadn't've": "had not have",
            "hasn't": "has not",
            "haven't": "have not",
            "he'd": "he had / he would",
            "he'd've": "he would have",
            "he'll": "he shall / he will",
            "he'll've": "he shall have / he will have",
            "he's": "he has / he is",
            "how'd": "how did",
            "how'd'y": "how do you",
            "how'll": "how will",
            "how's": "how has / how is / how does",
            "I'd": "I had / I would",
            "I'd've": "I would have",
            "I'll": "I shall / I will",
            "I'll've": "I shall have / I will have",
            "I'm": "I am",
            "I've": "I have",
            "isn't": "is not",
            "it'd": "it had / it would",
            "it'd've": "it would have",
            "it'll": "it shall / it will",
            "it'll've": "it shall have / it will have",
            "it's": "it has / it is",
            "let's": "let us",
            "ma'am": "madam",
            "mayn't": "may not",
            "might've": "might have",
            "mightn't": "might not",
            "mightn't've": "might not have",
            "must've": "must have",
            "mustn't": "must not",
            "mustn't've": "must not have",
            "needn't": "need not",
            "needn't've": "need not have",
            "o'clock": "of the clock",
            "oughtn't": "ought not",
            "oughtn't've": "ought not have",
            "shan't": "shall not",
            "sha'n't": "shall not",
            "shan't've": "shall not have",
            "she'd": "she had / she would",
            "she'd've": "she would have",
            "she'll": "she shall / she will",
            "she'll've": "she shall have / she will have",
            "she's": "she has / she is",
            "should've": "should have",
            "shouldn't": "should not",
            "shouldn't've": "should not have",
            "so've": "so have",
            "so's": "so as / so is",
            "that'd": "that would / that had",
            "that'd've": "that would have",
            "that's": "that has / that is",
            "there'd": "there had / there would",
            "there'd've": "there would have",
            "there's": "there has / there is",
            "they'd": "they had / they would",
            "they'd've": "they would have",
            "they'll": "they shall / they will",
            "they'll've": "they shall have / they will have",
            "they're": "they are",
            "they've": "they have",
            "to've": "to have",
            "wasn't": "was not",
            "we'd": "we had / we would",
            "we'd've": "we would have",
            "we'll": "we will",
            "we'll've": "we will have",
            "we're": "we are",
            "we've": "we have",
            "weren't": "were not",
            "what'll": "what shall / what will",
            "what'll've": "what shall have / what will have",
            "what're": "what are",
            "what's": "what has / what is",
            "what've": "what have",
            "when's": "when has / when is",
            "when've": "when have",
            "where'd": "where did",
            "where's": "where has / where is",
            "where've": "where have",
            "who'll": "who shall / who will",
            "who'll've": "who shall have / who will have",
            "who's": "who has / who is",
            "who've": "who have",
            "why's": "why has / why is",
            "why've": "why have",
            "will've": "will have",
            "won't": "will not",
            "won't've": "will not have",
            "would've": "would have",
            "wouldn't": "would not",
            "wouldn't've": "would not have",
            "y'all": "you all",
            "y'all'd": "you all would",
            "y'all'd've": "you all would have",
            "y'all're": "you all are",
            "y'all've": "you all have",
            "you'd": "you had / you would",
            "you'd've": "you would have",
            "you'll": "you shall / you will",
            "you'll've": "you shall have / you will have",
            "you're": "you are",
            "you've": "you have"
           }
        self.extra_punctuations = ['', '.', '``', '...', '\'s', '--', '-', 'n\'t', '_', '–', '&']
        self.stopword_list = stopwords.words('english') + list(string.punctuation) + self.extra_punctuations + ['u', 'the', 'us',
                                                                                                      'say', 'that',
                                                                                                      'he', 'me', 'she',
                                                                                                      'get', 'rt', 'it',
                                                                                                      'mt', 'via',
                                                                                                      'not', 'and',
                                                                                                      'let', 'so',
                                                                                                      'say', 'dont',
                                                                                                      'use', 'you']

    def clean_text(self,data):
        # wordnet_lemmatizer = WordNetLemmatizer()
        # stemmer = PorterStemmer()
        tokenizer = TweetTokenizer()
        data = unidecode(data)
        data = self.expandContractions(data)
        tokens = tokenizer.tokenize(data)
        data = ' '.join([tok for tok in tokens if len(tok) > 2 if tok not in self.stopword_list and not tok.isdigit()])
        data = re.sub('\b\w{,2}\b', '', data)
        data = re.sub(' +', ' ', data)
        data = self.removeSpecialChars(data)
        data = self.remove_emoji(data)
        # data = [stemmer.stem(w) for w in data.split()]
        # return ' '.join([wordnet_lemmatizer.lemmatize(word) for word in data])
        return data

    def expandContractions(self,text):
        c_re = re.compile('(%s)' % '|'.join(self.cList.keys()))
        def replace(match):
            return self.cList[match.group(0)]

        return c_re.sub(replace, text)

    def remove_emoji(self,string):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', string)

    def remove_punctuations(self,data):
        punct_tag = re.compile(r'[^\w\s]')
        data = punct_tag.sub(r'', data)
        return data

    def removeSpecialChars(self,data):
        '''
        Removes special characters which are specifically found in tweets.
        '''
        # Converts HTML tags to the characters they represent
        soup = BeautifulSoup(data, "html.parser")
        data = soup.get_text()

        # Convert www.* or https?://* to empty strings
        data = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', data)

        # Convert @username to empty strings
        data = re.sub('@[^\s]+', '', data)

        # remove org.apache. like texts
        data = re.sub('(\w+\.){2,}', '', data)

        # Remove additional white spaces
        data = re.sub('[\s]+', ' ', data)

        data = re.sub('\.(?!$)', '', data)

        # Replace #word with word
        data = re.sub(r'#([^\s]+)', r'\1', data)

        return data

    def remove_nonenglish_charac(self,string):
        return re.sub('\W+', '', string)
