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

def applyLDA(cleanDocs, k, p):
    """
    apply the model to the data: construct doc-term matrix,
    convert dictionary into bag-of-words and apply the LDA model.
    """

    dictionary = corpora.Dictionary(cleanDocs)
    corpus = [dictionary.doc2bow(doc) for doc in cleanDocs]
    model = gensim.models.ldamodel.LdaModel(corpus, num_topics = k, id2word = dictionary, passes = p)
    return(model)

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

def applyLDAvis(cleanDocs, k, p):
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
    pyLDAvis.save_html(data,str(k)+'vis.html')

if __name__ == '__main__':
    xmlFile = "English-Yusuf-Ali.xml"
    docs = parseXml(xmlFile)

    #initialize
    chunkSize = 100.0 # number of chunks to generate
    k = 50            # number of topics
    iterations = 20   # number of iterations

    cleanDocs= []
    for chapter in docs:
        cleanDoc = clean(chapter)
        cleanDocs.extend(cleanDoc)

    # apply POS filtering
    cleanDocs = applyPOS(cleanDocs)

    # create chunks of equal size
    cleanDocs = createChunks(cleanDocs, chunkSize)

    # apply LDA and create display
    for t in range(10,k):
        applyLDAvis(cleanDocs, k, iterations)
