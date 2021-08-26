#!/bin/sh
# Run all the steps to go from a chapter aligned file to a sentence aligned one.

echo "Filtering..."
python filter.py en.txt > en.txt.filter
python filter.py fr.txt > fr.txt.filter
echo "   Done."

echo "Converting to 1 sent per line..."
echo "en"
python to_sent_per_line.py en.txt.filter en
echo "fr"
python to_sent_per_line.py fr.txt.filter fr
echo "   Done."

echo "Translating..."
echo "en"
for file in en/*; do
    python translate.py $file en fr > ${file}.fr
done

echo "fr"
for file in fr/*; do
    python translate.py $file fr en > ${file}.en
done
echo "   Done."

echo "Aligning..."
rm -rf aligned
mkdir aligned
for file in en/*.txt; do
   ./Bleualign/bleualign.py -s $file -t fr/`basename $file` --srctotarget ${file}.fr --targettosrc fr/`basename $file`.en -o aligned/`basename $file`
done
echo "   Done."
