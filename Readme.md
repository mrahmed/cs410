## Apply LDA Topic Model to Quranic Text

In `main.py`, we apply a probabilistic statistical language model (LDA) to discover topics in the Quran.

## Script Actions

`main.py` perfoms the following actions:

- Parse the date from the XML file
- Clean the data by:
  * Tokanization
  * Lower casing
  * PoS filtering
  * Stop word removal
  * Punctuation removal
  * Special character removal
  * Apply LDA model using a number of topics and iterations
  * Visualize the output using LDAviz

## References

- https://stackoverflow.com/questions/4328500/how-can-i-strip-all-punctuation-from-a-string-in-javascript-using-regex
