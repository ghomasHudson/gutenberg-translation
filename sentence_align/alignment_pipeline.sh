#!/bin/sh
# Run all the steps to go from a chapter aligned file to a sentence aligned one.

# Needs one cmdline param: filename to convert
die () {
    echo >&2 "$@"
    exit 1
}
[ "$#" -eq 1 ] || die "1 argument required, $# provided"
[[ $1 == *".en."* ]] || die "$1 is not the English version"

fr=$(echo "$1" | sed "s/.en/.fr/")
cp $1 "tmp/en.txt"
cp $fr "tmp/fr.txt"

echo "Filtering..."
python filter.py /tmp/en.txt > /tmp/en.txt.filter
python filter.py /tmp/fr.txt > /tmp/fr.txt.filter
echo "   Done."

echo "Converting to 1 sent per line..."
echo "en"
source env/bin/activate
python to_sent_per_line.py /tmp/en.txt.filter en
echo "fr"
python to_sent_per_line.py /tmp/fr.txt.filter fr
deactivate
echo "   Done."

echo "Translating..."
echo "en"
source ../env/bin/activate
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

# Merge
en_out="$(basename $1).aligned"
fr_out="$(basename $fr).aligned"
echo $en_out
echo $fr_out

echo -n "" > $en_out
for file in en/*.txt; do
    sed '1s/^/[SECTION]\n/' $file >> $en_out
done
cat ../gutenberg_license.txt >> $en_out

echo -n "" > $fr_out
for file in fr/*.txt; do
    sed '1s/^/[SECTION]\n/' $file >> $fr_out
done
cat ../gutenberg_license.txt >> $fr_out

echo "Saved to $en_out, $fr_out"
