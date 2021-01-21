# excRef
Automatic reference tracking.

Converts bibliography into summarized and translated text

**Please note that this script processes pdf files from untrusted sources.**

## Usage
Check out main.py
```
bibliography = {
    "some_index_1": "Some title, Author, Journal, Kewords,... ",
    "some_index_2": "Some title, Author, Journal, Kewords,... ",
    "some_index_3": "Some title, Author, Journal, Kewords,... "
}
gather(bibliography, target_lang="ko")
```

## Dependency
* Python 3.9.0 
* scholarly 
* title2bib
* scidownl
* bibtexparser
* textract
* pysummarization
* googletrans==4.0.0-rc1

```
pip install scholarly title2bib scidownl bibtexparser textract pysummarization googletrans==4.0.0-rc1
```
