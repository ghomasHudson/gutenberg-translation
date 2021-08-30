'''Convert document to a one-sent-per-line format'''

import argparse
import spacy
import time
from deep_translator import GoogleTranslator

langs = GoogleTranslator.get_supported_languages(as_dict=True)
langs = list(langs.keys()) + list(langs.values())

parser = argparse.ArgumentParser()
parser.add_argument("input_file", type=argparse.FileType('r'))
parser.add_argument("srclang", type=str, choices=langs)
parser.add_argument("tgtlang", type=str, choices=langs)
args = parser.parse_args()

translator = GoogleTranslator(source=args.srclang, target=args.tgtlang)

# Chunk into max 5000
lines = args.input_file.readlines()
chunks = []
new_chunk = ""
for line in lines:
    if len(new_chunk) + len(line) < 5000:
        new_chunk += line
    else:
        chunks.append(new_chunk)
        new_chunk = line

for chunk in chunks:
    print(translator.translate(chunk))
    time.sleep(2)
