## Apply LDA Topic Model to Quranic Text

In `main.py`, we apply a probabilistic language model (LDA) to discover topics in the Quran. The Quran consists of 114 chapters which in turn
consist of verses. In the Quran, a topic could repeat in different chapters and sometimes in different contexts. While a topic starts in one verse, another
topic may start immediately in the next verse. Thus, a topic may start in the earlier chapters of the Quran and may end in the middle or last chapters of the Quran. This presents a challenge to the readers who would like to familiarize themselves with the topics discussed in the Quran. A reader may need to read the Quran several times in order to develop basic knowledge of the Quranic topics.

The objective of this project is to apply a topic model, LDA, to the Quran text. The result of the project is a visualization that allows users to explore the Quranic topics represented as groups of words. Since topics are represented by groups of words, users can select certain topic words to form search strings which then can be used on web search engines, like Google, to find further details on the topic.

For further details on the project, please read [`docs/project_report.pdf`](docs/project_report.pdf).


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

Because the chapters are of varrying lengths (some of them are few sentences and others are many paragraphs), all chapters had to be concatenated into a single unit of text and then re-partitioned into a nearly equal sized chuncks of text. To perform this transformation, `createChunks` function was used. Since there are **114** chapters in the Quran, **100** chunks was close enough to the original number of chapters.

**Note:** After experimenting with the number of chunks, **100** was determined to provide the most optimal results.


### Parsing the data

The dataset is contained in a single XML file, `English-Yusuf-Ali.xml`. The XML root includes **114** chapters which in turn include a varrying number of verses. Each verse is a single unit of text data. `ParseXML` function is used to parse the data. It also removes some special characters (`\t` and `\n`) as well as re-formats the occurnace of other characters (`.` and `-`). This cleanning and reformatting takes place during the parsing phase because it is not possible to do during the tokenization phase as it would change the form of some words. For instance, in the raw format of the data, there is no space between a `.` and the word following it (example: "*yesterday.He*"). It is important to add a space after the period to avoid having "*yesterday.He*" as a single word during the tokenization phase.

The steps to parsing the data are:

- Get the root of the XML tree
- Iterate through all children chapters
  * For each child, iterate through and concatenate its children verses to form a document represtening a complete chapter
- Return all documents (chapters), a total of **114** chapters


### Cleaning the data

Most of the document cleaning work is happening in this phase. There are a number of functions used together to complete the cleaning task:

- `clean` function does most of the work of cleaning the documents. It removes all punctuation, digits and stop words as well as special characters used to indicate Arabic phonetic guidance marks.
- `applyPOS` and `filterByPOS` are used to clean parts of speech.

### Applying LDA Model and Visualize the Topics

`applyLDAviz` function is used to apply the LDA model to the data and visualize the topics. We generated **49** models with topic numbers ranging from **2** to **50**. All the results are visualized and saved in the `vis1` and `vis1` folders. `vis2` contains the models that were applied to the original chapters; while `vis1` contains the models applied to the equal size chunks of text. We have added an iframe slider in each folder to make it more convenient for users to explore the different models. Use `vis#\quranTopicModelSlider.html` to explore the models in each folder. 

![screenshot of the iframe slider `quranTopicModelSlider.html`](images/iframeModelSlider.PNG)

We also added `index.html` to allow users to explore the models in either folder from the same page. Use the check-box to switch between models applied to the original chapters and models applied to the equal size chunks of text.

![screenshot of the iframe slider `index.html`](images/indexSlider.PNG)

### Visual Definitions

Below is a simple list of LDAviz definitions:

- The size of a bubble reflects the number of words in a topic.
- The distance between bubbles reflects how different or similar two topics are.
- Hovering over a word highlights other topics the word is a member of.

For richer details on LDAvis visual definitions, please read the section **Definitions of Visual Elements in LDAvis** of [`docs/project_report.pdf`](docs/project_report.pdf).


## Software Usage

In order to use the visualization of the topics:

- Download this repository to your desktop
- Unzip the content of the repository
- Open index.html to start exploring the topics

**Note:** `index.html`, `vis1` and `vis2` should be saved in the same dirctory.

### A Use Case

A very immediate use case is to:
- Explore the topics using the provided visualization
- Find a topic of interest
- Use certain topic words to form a search string
- Perform a web search on this string to explore further details on the topic


To experience this use case, go through these steps to discover a story of Moses:

- Make sure you check the checkbox that allows you to switch to *equal size chunks of text*.
- Move the topic slider to select the model with **37** topics.
- Select topic number **10**
- Set lambda value to **1**
- Form a search string using the listed topic words `"moses, pharaoh, sorcerers"`
- Perform a web search on Google using this search string

The search will return pages that further discuss this story of Moses.

## Team Contribution

Names of team members:
- Muhammad Ahmed
- Kahtan Al Jewary

The team members completed the project concurrently in a balanced manner and without deliberate assignments of the project tasks. Team members have spent equal efforts on this project.
 

## API References

- [Gensim Library](https://radimrehurek.com/gensim/apiref.html)
- [Removing Punctuation using Regex](https://stackoverflow.com/questions/4328500/how-can-i-strip-all-punctuation-from-a-string-in-javascript-using-regex)
- [NLTK Library](http://www.nltk.org/api/nltk.html)
- [pyLDAviz](https://github.com/bmabey/pyLDAvis)
