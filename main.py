'''Find english/translated book pairs'''
import sqlite3
import re
from fuzzywuzzy import fuzz
import numpy
import csv
import json
import os

if not os.path.exists("gutenbergindex.db"):
    from gutenbergpy.gutenbergcache import GutenbergCache
    GutenbergCache.create(refresh=True, download=True, unpack=True, parse=True, cache=True, deleteTemp=True)

con = sqlite3.connect('gutenbergindex.db')
cur = con.cursor()

from deep_translator import GoogleTranslator
translator = GoogleTranslator(source="auto", target="en")

cache = {}
with open("cache.txt") as f:
    reader = csv.reader(f)
    for row in reader:
        cache[row[0]] = row[1]
cache_writer = csv.writer(open("cache.txt", 'a'))

# Write old cache
# for k in cache:
#     cache_writer.writerow([k, cache[k]])


json_file = open("book_pairs.json", 'w')

def closest_match(q, books):
    ratios = []
    for b in books:
        ratios.append(fuzz.token_sort_ratio(q.lower(), b.lower()))
    idx = numpy.argmax(ratios)
    if ratios[idx] < 80:
        return None
    print("ratio", ratios[idx])
    # ratios = list(zip(books,ratios))
    # ratios = sorted(ratios, key=lambda x:x[1])
    # print(ratios)
    return books[idx]
i = 0
for auth_id, auth_name in list(cur.execute("SELECT * from authors;")):
    has_en = False
    has_non_en = False
    books = []
    # if "Dickens, Charles" != auth_name:
    #     continue
    # print(auth_id, auth_name)
    for book_id in list(cur.execute("SELECT bookid from book_authors WHERE authorid="+str(auth_id)+";")):
        book_id = book_id[0]
        book = list(cur.execute("SELECT * from books WHERE id="+str(book_id)+";"))[0]
        book = {
            "id": book[7],
            "language": list(cur.execute("SELECT name FROM languages WHERE id="+str(book[5])+";"))[0][0],
            "title": list(cur.execute("SELECT name FROM titles WHERE bookid="+str(book_id)+";"))[0][0]
        }
        books.append(book)
        if book["language"] == "en":
            has_en = True
        else:
            has_non_en = True
    if has_non_en and has_en:
        book_titles = [b["title"] for b in books if b["language"] == "en"]
        for book in books:
            if book["language"] != "en":
                # Check if in cache
                if book["title"] in cache.keys():
                    title_translated = cache[book["title"]]
                else:
                    title_translated = translator.translate(book["title"])
                    cache[book["title"]] = title_translated
                    cache_writer.writerow([book["title"], title_translated])
                    i += 1
                # print(book["title"] + "|" + title_translated)
                match = closest_match(title_translated, book_titles)
                if match is not None:
                    print(book["title"], "|", title_translated, "|", match)
                    for b in books:
                        if b["title"] == match:
                            english_book = b
                            break
                    line = json.dumps({
                        "english_book": english_book,
                        "translated_book": book
                    })
                    json_file.write(line + "\n")
                    print(line)
                    # print("match:", match)
                # if i == 10:
                #     import sys;sys.exit()

            # print("\t", book)


