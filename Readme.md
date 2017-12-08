## Apply LDA Topic Model to Quranic Text

In `main.py`, we apply a probabilistic statistical language model (LDA) to discover topics in the Quran.

## Script Actions

`main.py` perfoms the following actions:

- Parse the data XML file
- Clean the data by:
  * Tokanization
  * Lower casing
  * PoS filtering
  * Stop word removal
  * Punctuation removal
  * Special character removal
- Apply LDA to the data
- Visualize the topics

### Partitioning the data

Because the chapters are of varrying lengths (some of them are few senetences and others are many paragraphs), all chapters had to be concatenated into a single unit of text and then re-partitioned into a nearly equal sized chuncks of text. To perform this transformation, `createChunks` function was used. Since there are **114** chapters in the Quran, **100** chunks was close enough to the original number of chapters.

**Note:** After experimenting with the number of chunks, **100** was determined to provide the most optimal results.


### Parsing the data

The dataset is contained in a single XML file, `English-Yusuf-Ali.xml`. The XML root includes **114** chapters which in turn include a variant number of verses. Each verse is a single unit of text data. `ParseXML` function parses the data. It also removes some special characters as well as re-format the occurnace of other characters. This cleanning and reformatting takes place during the parsing phase because it is not possible to do during the tokenization phase as some words end up being a single word because, for example, there is no space between a period `.` and the following word.

The data is parsed in the following way:

- Get the root of the XML tree
- Iterate through all childern chapters
  * For each child, iterate through and concatenate its childern verses to form a document represtening a complete chapter
- Return all documents (chapters), a total of 114 chapters


### Cleaning the data

Most of the document cleaning work is happening in this phase. There are a number of functions used together to complete the cleaning task:

- `clean` function does most of the work of cleaning the documents. It removes all punctuation, digits, stop words and special characters used to indicate Arabic phonetic guidance marks.
- `applyPOS` and `filterByPOS` are used to clean parts of speech.

### Applying LDA Model and Visualize the Topics

`applyLDAviz` function is used to apply the LDA model to the data and visualize the topics. We generated 40 models with topic numbers ranging from **10** to **49**. All the results are visualized and saved in the `models` folder. We have added an iframe slider to make it more convenient for users to explore the different models. Use `models\quranTopicModelSlider.html` to explore the models. 

![screenshot of the iframe slider](https://github.com/mrahmed/cs410/blob/master/iframeSlider.PNG)


## API References

- [Gensim Library](https://radimrehurek.com/gensim/apiref.html)
- [Removing Punctuation using Regex](https://stackoverflow.com/questions/4328500/how-can-i-strip-all-punctuation-from-a-string-in-javascript-using-regex)
- [NLTK Library](http://www.nltk.org/api/nltk.html)
- [pyLDAviz](https://github.com/bmabey/pyLDAvis)
