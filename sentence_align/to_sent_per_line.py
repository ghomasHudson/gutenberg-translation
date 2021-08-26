'''Convert document to a one-sent-per-line format'''

import argparse
import spacy

lang_to_model = {
    "en": "en_core_web_sm",
    "fr": "fr_core_news_sm",
    # "en": "en_core_web_trf",
    # "fr": "fr_dep_news_trf"
}

parser = argparse.ArgumentParser()
parser.add_argument("input_file", type=argparse.FileType('r'))
parser.add_argument("lang", type=str, choices=list(lang_to_model.keys()))
args = parser.parse_args()

nlp = spacy.load(lang_to_model[args.lang])
doc = nlp(args.input_file.read())

for sent in doc.sents:
    text = str(sent).replace("\n", " ").strip()
    if text != "":
        print(text)
