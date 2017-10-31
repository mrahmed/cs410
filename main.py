import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim import corpora, models
import gensim
import string
import re
import nltk

def parseXml(xmlFile):
    """
    The passed xml file consists of 114 chapters.
    Each chapter consists of a number of verses.
    The function does the following:
        - Parse xml file into element tree
        - Go through each element
        - Extract and join each verses's text
        - Assign the joined text to "doc"
        - Remove any instances of "\n" and "\t"
        - Return a list of documents
    Each docment contains the full text of a chapter.

    To re-map a doc to a chapter, use (index of doc + 1)
    as the id. Example: the first chapter has a Chapter
    id of 1 in the xml file and an index of 0 in the "docs"
    list of documents.
    """
    tree = ET.parse(xmlFile)
    root = tree.getroot()

    docs = []
    for child in root:
	    doc = "".join(child.itertext())
	    doc = doc.replace("\n", "")
	    doc = doc.replace("\t", "")
	    doc = doc.replace(".", ". ")

	    docs.append(doc)
    return(docs)



def clean(doc):
    """
    To clean the documents:
        - Tokenize each document
        - Remove stop words from each document
        - Remove punctuation
    """
    i = 0
    stop = set(stopwords.words('english')) #stop words
    allow = ["all","lord","your"]
    punc = set(string.punctuation)
    moreStop = ["ye", "shall", "thee", "thy", "thou", "say", "said", "us", "indeed", "may", "hath"]
    for word in moreStop:
        stop.add(word) #add more stop words

    # https://stackoverflow.com/questions/4328500/how-can-i-strip-all-punctuation-from-a-string-in-javascript-using-regex
    regex = re.compile('[%s]' % re.escape("!\"#$%&()*+,./:;<=>?@[\]^_`{|}~"))
    cleanDoc = doc.lower()  # convert to lower
    cleanDoc = re.sub('(?<! )(?=[.,;!?()])|(?<=[.,;!?()])(?! )', r' ', cleanDoc)
    cleanDoc = regex.sub('', cleanDoc) #remove punctuation
    cleanDoc = ''.join(i for i in cleanDoc if not i.isdigit()) #remove remove any digit
    cleanDoc = cleanDoc.split() #split into list
    cleanDoc = [word for word in cleanDoc if (word not in stop or word in allow)]
    cleanDoc = [word for word in cleanDoc if word not in punc]
    return(cleanDoc)
xmlFile = "English-Yusuf-Ali.xml"
docs = parseXml(xmlFile)
docs.insert(0, "")# #shift index to match with chapter index
cleanDocs= []
posDocs= []
for x in range(1, 114):
    cleanDoc = clean(docs[x])
    cleanDoc = cleanDoc[1:]  # remove first element which is index
    posDocs.extend(nltk.pos_tag(cleanDoc))
    cleanDocs.extend(cleanDoc)
n = 10.0 # number of chunks to generate
chunk = int(round(len(cleanDocs)/n))
chunks = [cleanDocs[i:i+chunk] for i in range(0,len(cleanDocs),chunk)]
#print(cleanDocs)
print(posDocs)
print(cleanDocs)
"""

1-Al-Fatihah 2-Al-Baqarah 3-Al-'Imran 4-An-Nisa' 5-Al-Ma'idah 6-Al-An'am 7-Al-A'raf 8-Al-Anfal 9-Al-Bara'at / At-Taubah 10-Yunus 11-Hud 12-Yusuf 13-Ar-
Ra'd 14-Ibrahim 15-Al-Hijr 16-An-Nahl 17-Bani Isra'il 18-Al-Kahf 19-Maryam 20-Ta Ha 21-Al-Anbiya' 22-Al-Hajj 23-Al-Mu'minun 24-An-Nur 25-Al-Furqan 26-Ash-
Shu'ara' 27-An-Naml 28-Al-Qasas 29-Al-'Ankabut 30-Ar-Rum 31-Luqman 32-As-Sajdah 33-Al-Ahzab 34-Al-Saba' 35-Al-Fatir 36-Ya Sin 37-As-Saffat 38-Sad 39-Az-
Zumar 40-Al-Mu'min 41-Ha Mim 42-Ash-Shura 43-Az-Zukhruf 44-Ad-Dukhan 45-Al-Jathiyah 46-Al-Ahqaf 47-Muhammad 48-Al-Fath 49-Al-Hujurat 50-Qaf 51-Ad-Dhariyat
52-At-Tur 53-An-Najm 54-Al-Qamar 55-Ar-Rahman 56-Al-Waqi'ah 57-Al-Hadid 58-Al-Mujadilah 59-Al-Hashr 60-Al-Mumtahanah 61-As-Saff 62-Al-Jumu'ah 63-Al-
Munafiqun 64-At-Taghabun 65-At-Talaq 66-At-Tahrim 67-Al-Mulk 68-Al-Qalam 69-Al-Haqqah 70-Al-Ma'arij 71-Nuh 72-Al-Jinn 73-Al-Muzzammil 74-Al-Muddaththir
75-Al-Qiyamah 76-Al-Insan 77-Al-Mursalat 78-An-Naba' 79-An-Nazi'at 80-'Abasa 81-At-Takwir 82-Al-Infitar 83-At-Tatfif 84-Al-Inshiqaq 85-Al-Buruj 86-At-
Tariq 87-Al-A'la 88-Al-Ghashiyah 89-Al-Fajr 90-Al-Balad 91-Ash-Shams 92-Al-Lail 93-Ad-Duha 94-Al-Inshirah 95-At-Tin 96-Al-'Alaq 97-Al-Qadr 98-Al-Bayyinah
99-Al-Zilzal 100-Al-'Adiyat 101-Al-Qari'ah 102-At-Takathur 103-Al-'Asr 104-Al-Humazah 105-Al-Fil 106-Al-Quraish 107-Al-Ma'un 108-Al-Kauthar 109-Al-Kafirun
110-An-Nasr 111-Al-Lahab 112-Al-Ikhlas 113-Al-Falaq 114-An-Nas

"""

