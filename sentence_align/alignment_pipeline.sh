#!/bin/sh

python filter.py en.txt > en.txt.filter
python filter.py fr.txt > fr.txt.filter

python to_sent_per_line.py en.txt.filter en > en.txt.sent
python to_sent_per_line.py fr.txt.filter fr > fr.txt.sent

python translate.py en.txt.filter en fr > en.txt.fr
python to_sent_per_line.py fr.txt.filter fr en > fr.txt.en

./Bleualign/bleualign -s en.txt.sent -t fr.txt.sent --srctotarget en.txt.fr --targettosrc fr.txt.en -o output
