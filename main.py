# from scihub2pdf.download import  get_bib_from_title
from title2bib.crossref import get_bib_from_title
from scholarly import scholarly
from scidownl.scihub import *
import bibtexparser
import os
import textract
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
from googletrans import Translator  # pip install googletrans==4.0.0-rc1

out_dir = lambda x: os.path.join('./pdf/', x)


def _get_pdf(k, title):
    # Skip if exists
    if os.path.isdir(out_dir(k)) and os.listdir(out_dir(k)):
        return os.path.join(out_dir(k), os.listdir(out_dir(k))[0])
    # Normalize title
    google_search = scholarly.search_pubs(title)
    google_result = next(google_search)
    print(title)
    title = google_result['bib']['title'] + ' ' + (' '.join(google_result['bib']['author']))
    print(title)
    # Get DOI
    try:
        found, bib_string = get_bib_from_title(title)
    except Exception as e:
        print("Error while getting DOI", e)
        return None
    # Download
    if found:
        bib = bibtexparser.loads(bib_string).entries
        if bib and ("doi" in bib[0]) and (bib[0]['ENTRYTYPE'] == 'article'):
            doi = bib[0]["doi"]
            try:
                SciHub(doi, out_dir(k)).download(choose_scihub_url_index=3)
            except Exception as e:
                print("Error while downloading", e)
                return None
            pdf = os.path.join(out_dir(k), os.listdir(out_dir(k))[0]) if os.listdir(out_dir(k)) else None
            return pdf
        else:
            print(bib)
            print("\tAbsent DOI")
    return None


def _set_summarizer():
    auto_abstractor = AutoAbstractor()
    auto_abstractor.tokenizable_doc = SimpleTokenizer()
    auto_abstractor.delimiter_list = [". "]  # [".", "\n"]
    abstractable_doc = TopNRankAbstractor()
    abstractable_doc.set_top_n(10)
    return lambda text: auto_abstractor.summarize(text, abstractable_doc)["summarize_result"]


def gather(bibliography, target_lang, skip_download=False):
    summarize = _set_summarizer()
    translator = Translator()

    pdfs = {k: _get_pdf(k, v) for k, v in bibliography.items()}
    texts = {k: str(textract.process(pdf), 'utf-8').replace('\n', ' ') for k, pdf in pdfs.items() if pdf}
    summaries = {k: '\n'.join(summarize(text)) for k, text in texts.items()}
    translates = {k: translator.translate(text, src='en', dest=target_lang).text for k, text in summaries.items()}

    for k, text in translates.items():
        print("====")
        print(k)
        print(text)
        print("====")


bibliography = {
    "12_1": "",
}

gather(bibliography, target_lang="ko", skip_download=False)
# gather(bibliography, target_lang="ko", skip_download=True)

