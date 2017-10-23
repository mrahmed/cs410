import xml.etree.ElementTree as ET
import nltk

def parseXml(xmlFile):
    """
    the passed xml file consists of 114 chapters.
    each chapter consists of a number of verses.
    the function does the following:
        - parse xml file into element tree
        - go through each element
        - extracts and joins each verses's text
        - assign the joined text to "doc"
        - remove any instances of "\n" and "\t"
        - return a list of documents
    each docment contains the full text of a chapter.

    to re-map a doc to a chapter, use (index of doc + 1)
    as the id. example: the first chapter has a Chapter
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

	    docs.append(doc)
    return(docs)


xmlFile = "English-Yusuf-Ali.xml"
docs = parseXml(xmlFile)

print(docs)
print(len(docs))

