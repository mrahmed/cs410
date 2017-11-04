import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim import corpora, models
import gensim
import string
import re
import nltk
import pyLDAvis.gensim

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

def filterByPOS(posTags, filter):
    filteredArr = []
    for w in posTags:
        #print(w[0])
        #print(w[1])
        for f in filter:
            if w[1] == f:
                filteredArr.append(w[0])
    return filteredArr

def clean(doc):
    """
    To clean the documents:
        - Tokenize each document
        - Remove stop words from each document
        - Remove punctuation
    """
    i = 0
    stop = set(stopwords.words('english')) #stop words
    allow = ["lord"]
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

def applyLDA(cleanDocs, k, p):
    """
    Apply the model to the data:
        - Construct doc-term matrix
        - Convert dictionary into bag-of-words
        - Apply the LDA model
    """
    dictionary = corpora.Dictionary(cleanDocs)
    corpus = [dictionary.doc2bow(doc) for doc in cleanDocs]
    model = gensim.models.ldamodel.LdaModel(corpus, num_topics = k, id2word = dictionary, passes = p)

    return(model)

def applyLDAvis(cleanDocs, k, p):
    """
    Apply the model to the data:
        - Construct doc-term matrix
        - Convert dictionary into bag-of-words
        - Apply the LDA model
    """

    dictionary = corpora.Dictionary(cleanDocs)
    corpus = [dictionary.doc2bow(doc) for doc in cleanDocs]
    model = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=30)
    model.save('topic.model')
    lda = models.LdaModel.load('topic.model')
    data = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
    pyLDAvis.save_html(data,'vis.html')

if __name__ == '__main__':
    xmlFile = "English-Yusuf-Ali.xml"
    docs = parseXml(xmlFile)
    docs.insert(0, "")# #shift index to match with chapter index
    cleanDocs= []
    posDocs= []
    for x in range(110, 114):
        cleanDoc = clean(docs[x])
        cleanDoc = cleanDoc[1:]  # remove first element which is index
        cleanDocs.extend(cleanDoc)
    filter =["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "PRP", "PRP$", "RB", "RBR", "RBS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WP", "WP$", "WRB"]
    cleandocs = filterByPOS(nltk.pos_tag(cleanDoc), filter)
    n = 100.0 # number of chunks to generate
    chunk = int(round(len(cleanDocs)/n))
    chunks = [cleanDocs
    [i: i + chunk] for i in range(0, len(cleanDocs), chunk)]
    cleanDocs = chunks
    applyLDAvis(cleanDocs, 10, 30)

