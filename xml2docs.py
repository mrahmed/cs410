import xml.etree.ElementTree as ET

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

	    docs.append(doc)
    return(docs)


xmlFile = "English-Yusuf-Ali.xml"
docs = parseXml(xmlFile)

print(docs[0])
