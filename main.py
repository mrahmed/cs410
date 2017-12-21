import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim import corpora, models
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import os
import string
import re
import nltk
import pyLDAvis.gensim

def parseXml(xmlFile):
    """
    the passed xml file consists of 114 chapters.
    each chapter consists of a number of verses.
    """
    tree = ET.parse(xmlFile)
    root = tree.getroot()

    docs = []
    for child in root:
       doc = "".join(child.itertext())
       doc = doc.replace("\n", "")
       doc = doc.replace("\t", "")
       doc = doc.replace(".", ". ")
       doc = doc.replace("re-", "re")

       docs.append(doc)
    return(docs)

def filterByPOS(posTags, filter):
    filteredArr = []
    for w in posTags:
        for f in filter:
            if w[1] == f:
                filteredArr.append(w[0])
    return filteredArr

def clean(doc):
    """
    to clean a document: tokenize, remove stop words,
    remove punctuation, lowercase terms, remove digits
    and remove special characters.
    """
    i = 0
    stop = set(stopwords.words('english'))
    moreStop = ["ye", "shall", "thee", "thy", "thou", "say", "one"]
    moreStop.extend(["said", "us", "indeed", "may", "hath", "two"])
    moreStop.extend(["allah", "lord", "would", "unto", "also", "could"])
    moreStop.extend(["things", "ah"])
    for word in moreStop:
        stop.add(word)

    # remove all punctuation and digits
    regex = re.compile('[%s]' % re.escape("!\"#$%&()*+,./:;<=>?@[\]^_`´{|}~-"))
    cleanDoc = doc.lower()
    cleanDoc = re.sub('(?<! )(?=[.,;!?()])|(?<=[.,;!?()])(?! )', r' ', cleanDoc)
    cleanDoc = regex.sub('', cleanDoc)
    cleanDoc = ''.join(i for i in cleanDoc if not i.isdigit())

    # convert into list and remove stopwords
    cleanDoc = cleanDoc.split()
    cleanDoc = [word for word in cleanDoc if (word not in stop)]

    # remove special characters (example: -word, word-, `word, word`)
    cleanDoc = [word.replace("-", "") if ("-" in [word[0], word[-1]]) else word for word in cleanDoc]
    cleanDoc = [word.replace("`", "") if ("`" in [word[0], word[-1]]) else word for word in cleanDoc]
    return(cleanDoc)

def applyPOS(cleanDocs):
    """
    apply POS filtering
    """

    filter =[]
    filter.extend(["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS"])
    filter.extend(["PRP", "PRP$", "RB", "RBR", "RBS", "VB", "VBD"])
    filter.extend(["VBG", "VBN", "VBP", "VBZ", "WP", "WP$", "WRB"])
    filter.extend(["IN", "LS", "MD", "WDH"])
    cleandocs = filterByPOS(nltk.pos_tag(cleanDocs), filter)
    return (cleanDocs)

def createChunks(cleanDocs, n):
    """
    create chunks of equal size
    """
    chunk = int(round(len(cleanDocs)/n))
    chunks = [cleanDocs [i: i + chunk] for i in range(0, len(cleanDocs), chunk)]
    return (chunks)

def applyLDAvis(cleanDocs, k, p, setNum):
    """
    apply the model to the data: construct doc-term matrix,
    convert dictionary into bag-of-words, apply the LDA model.
    """

    dictionary = corpora.Dictionary(cleanDocs)
    corpus = [dictionary.doc2bow(doc) for doc in cleanDocs]
    model = gensim.models.ldamodel.LdaModel(corpus, num_topics=k, id2word=dictionary, passes=p)
    model.save('topic.model')
    lda = models.LdaModel.load('topic.model')
    data = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
    whichVis = str(setNum)
    pyLDAvis.save_html(data,'vis'+whichVis+'/'+str(k)+'vis.html')
def check_path(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

if __name__ == '__main__':

   # create path if not exits
    check_path('vis1/')
    check_path('vis2/')

    xmlFile = "English-Yusuf-Ali.xml"
    docs = parseXml(xmlFile)

    #initialize
    chunkSize = 100.0 # number of chunks to generate
    k = 51            # number of topics
    iterations = 20   # number of iterations

 
    cleanDocs1= []
    cleanDocs2 = []
    for chapter in docs:
        cleanDoc = clean(chapter)
        cleanDoc = applyPOS(cleanDoc)
        # extend content to make chunks later
        cleanDocs1.extend(cleanDoc)
        # cleanDocs2 contain individual chapters
        cleanDocs2.append(cleanDoc)

    # apply POS filtering
    # create chunks of equal size
    cleanDocs1 = createChunks(cleanDocs1, chunkSize)
    # apply LDA and create display
    for t in range(2,k):
        applyLDAvis(cleanDocs1, t, iterations, 1)
        applyLDAvis(cleanDocs2, t, iterations, 2)
