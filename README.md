# autovoc

autovoc is a Python script which automatically generates gapfill exercises for English proficiency classes. The script randomly selects a word from a vocabulary list, finds the best natural language context for an exercise and then leaves out the word in that natural context. To help the student, a definition is given after the gap. An example for the word *excessive* is given below:
> Remove the first slice, then continue carving until approximately one third of the way down the ham. Cut down to the bone to avoid [excessive] (*beyond normal limits*) wastage.

Building and maintaining vocabulary exercises is a laborious job. autovoc aims to support teachers and assistants in creating new material by automating this job as much as possible. It does ***not*** aim to make instructors redundant. Bear in mind that autovoc is still in a proof-of-concept state.

## How does it work?

autovoc finds a natural context for a specific word from the [British National Corpus (BNC)](http://www.natcorp.ox.ac.uk/)  using the [SketchEngine](http://sketchengine.eu/) API. The best context is selected using the [GDEX system](https://www.sketchengine.eu/guide/gdex/), which is normally used to find the best example sentences for use in dictionary entries. The same system can be applied in this context, however. The definitions which are given as hints to the student are sourced from [WordNet](https://wordnet.princeton.edu/).

## Set-up

### autovoc

1. Clone the repository:  
    `git clone https://github.com/AntheSevenants/autovoc.git`
2. Navigate to the repository:  
    `cd autovoc`
3. Create a virtual environment:  
	`python3 -m venv venv`
4. Activate the virtual environment:  
	`source venv/bin/activate`
5. Install the dependencies:  
	`pip install -r requirements.txt`
6. Download the required wordnet files by executing the following command:  
    `python3 -c 'import nltk; nltk.download("wordnet");'`  
    You only need to do this once.

The virtual environment needs to be active in order to be able to run the script. You can check whether the virtual environment is activated by checking whether there is (venv) in front of your user@hostname.

### Word list

autovoc picks words from a word list to generate exercises for these words. Word lists are simple plain-text files with individual words on every line. For example:
```
airplane
disproportionate
fortunate
vigorous
convert
firefighter
```

### SketchEngine API key

autovoc requires an API key to communicate with SketchEngine.

1. [Generate an API key for SketchEngine.](https://www.sketchengine.eu/documentation/api-documentation/#toggle-id-1) Beware that SketchEngine is a paid product.
2. Save the API key to a file named `sketchengine_api_key` in the autovoc directory. Notice that this file has no extension.

## Running autovoc

You can run autovoc by entering `python3 autovoc.py <wordlist path> <exercise count>`. `<wordlist path>` is the path to your list of words (e.g. `wordlist.txt`). `<exercise count>` is the number of exercises you want to generate (i.e. how many words will be in the generated test, for example `10`). The command `python3 autovoc.py wordlist.txt 5` will generate a test for five random words from `wordlist.txt`. The current version of autovoc generates **four** exercises for each word, so you can pick the best exercise among these four suggestions yourself.

autovoc will output the exercises to the file `output.json` in the autovoc directory. The exercises are in the [JSON](https://en.wikipedia.org/wiki/JSON) format, so you can process the output yourself to make an online exercise, generate a PDF, etc. The output format is as follows:
```
[ 
    { "unit": "0",
	  "word": word,
	  "definition": definition,
      "synonyms": "",
	  "corpus": corpus_sentence
    },
    ...
]
```

For example:
```
[
    { "unit": "0",
      "word": "excessive",
      "definition": "beyond normal limits",
      "synonyms": "",
      "corpus": "Remove the first slice, then continue carving until approximately one third of the way down the ham. Cut down to the bone to avoid excessive wastage." 
    },
    ...
]
```

Notice that the attributes *unit* and *synonyms* are currently unused.

## Current issues

* autovoc is currently restricted to atomic words (ie. words which do not consist of multiple parts, such as *potato*). Words which consist of multiple parts (e.g. *town hall*) are currently not supported.
* Words can be [homonymous](https://en.wikipedia.org/wiki/Homonymy), and autovoc is blind to the different uses of a specific word. This means that autovoc will often pick the wrong definition from WordNet or generate an exercise for a word as a different part of speech.
* The definitions from WordNet are often of a lower quality standard. The definitions found in traditional dictionaries such as [Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/) or [Merriam-Webster](https://www.merriam-webster.com/) are of much higher quality. Merriam Webster has a [free API](https://dictionaryapi.com/) (which does seem to permit non-profit use), Cambridge Dictionary only has a paid API, regardless of your use. While the quality of dictionary definitions may be better, autovoc would still have to guess which definition applies to the specific use of the word you have intended.
* Corpus data is inherently messy. autovoc's natural language extracts include the sentence before the keyword, the sentence of the keyword and the sentence after the keyword. This might be too much or too little context, depending on the word and/or the text. This is also why autovoc currently proposes four exercises for each word. Manual review will always be necessary.
* autovoc does not keep track of which words have already been chosen. This means that you could theoretically generate the same exercise over and over again, especially if you have a small word list.
* SketchEngine is a paid product, which means that the use of autovoc has an upfront cost. This is no issue if your academic institution already provides access to SketchEngine, but it does exclude users who do not have this access. autovoc should ideally be able to access local corpora and apply GDEX locally.
* autovoc is currently set up to generate English vocabulary exercises, but there is no reason why it could not be adapted to generate vocabulary exercises for -- for example -- French, Dutch or Norwegian. The corpus would have to be changed, as well as the source for definitions, but the core concept would remain exactly the same.

If you want me to develop autovoc further, please [contact me](https://github.com/AntheSevenants).