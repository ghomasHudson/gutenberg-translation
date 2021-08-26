'''Remove bad characters'''
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("input_file", type=argparse.FileType('r'))
args = parser.parse_args()

text = args.input_file.read()
text = text.split("*** START: FULL LICENSE ***")[0]
text = text.replace("«", '"')
text = text.replace("»", '"')
text = text.replace("_", '')
text = text.replace("--", '')
text = text.replace("-", ' ')
print(text)
