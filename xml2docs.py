import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

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


def clean(docs):
    """
    To clean the documents:
        - Tokenize each document
        - Remove stop words from each document
    """
    stop = set(stopwords.words('english'))
    punc = set(string.punctuation)

    cleanDocs = []
    for doc in docs:
        tokenized = word_tokenize(doc)
        stopFree = [word for word in tokenized if word.lower() not in stop]
        puncFree = [word for word in stopFree if word not in punc]
        cleanDocs.append(puncFree)

    return(cleanDocs)


xmlFile = "English-Yusuf-Ali.xml"
docs = parseXml(xmlFile)
cleanDocs = clean(docs)

print(docs[0])
print(cleanDocs[0])
