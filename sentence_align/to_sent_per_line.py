'''Convert document to a one-sent-per-line format'''

import argparse
import spacy
import re
import shutil
import os

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

try:
    os.mkdir(args.lang)
except:
    shutil.rmtree(args.lang)
    os.mkdir(args.lang)
    pass

nlp = spacy.load(lang_to_model[args.lang])
chapters = args.input_file.read().split("[SECTION]")
chapters = [c for c in chapters if c.strip() != ""]

for i, chapter in enumerate(chapters):
    chapter = chapter.replace("*", "")
    chapter = chapter.replace("\n", " ").strip()
    doc = nlp(chapter)
    with open(os.path.join(args.lang, str(i) + ".txt"), 'w') as f:
        for sent in doc.sents:
            text = str(sent)
            text = text.replace("[SECTION]", ".EOA")
            if ".EOA" in text and text != ".EOA":
                text = text.replace(".EOA", ".EOA\n")
                text = re.sub("\n +", "\n", text)
            if text != "":
                print(text)
                f.write(text.strip() + "\n")
