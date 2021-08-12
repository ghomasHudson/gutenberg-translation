import requests
import re


def is_number_word(number_word, lang="en"):
    number_word = number_word.replace(" ", "-").lower()
    if number_word == "-":
        return False
    from num2words import num2words
    for l in [lang, "en"]:
        for i in range(100):
            try:
                if number_word in num2words(i, lang=l).split("-"):
                    return True
            except NotImplementedError:
                break

    return False

def get_text(book_id, lang="en"):
    print(book_id)

    for full_id in [str(book_id)+"-0", "pg"+str(book_id)]:
        num_id = full_id.split("-")[0]
        num_id = "".join([str(int(s)) for s in num_id if s.isdigit()])
        dir_str = "cache/epub" if "pg" in full_id else "files"

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        r = requests.get("https://www.gutenberg.org/"+dir_str+"/"+str(num_id)+"/"+str(full_id)+".txt", headers=headers)
        if r.status_code == 200:
            break
    from gutenberg_cleaner import simple_cleaner
    book = simple_cleaner(r.text)

    # print(book[:5000])
    chapters = [["START",[]]]
    new_chapter_title = "START"


    max_line_length = max([len(l) for l in book.split("\n")])

    for line in book.split("\n"):
        if "END OF THE PROJECT GUTENBERG EBOOK" in line:
            break
        lSplit = line.replace(".", "").replace("-", " ").split()
        if line == "" or len(lSplit) == 0:
            chapters[-1][-1].append("")
            # print()
            continue
        if len(lSplit) < 4 and len(lSplit) > 0 and (re.match("(^(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})\.?$)", lSplit[-1]) or re.match("^[0-9]+$", lSplit[-1]) or is_number_word(lSplit[-1], lang=lang)):
            # print("[DELETED:", line,"]")
            new_chapter_title = line.strip()
            chapters.append([new_chapter_title, []])
        elif lSplit[0].lower() in ["preface", "act", "chapter", "chaptre", "stave", "preface", "introduction", "epilogue", "introduction", "scene", "scène"] or (len(lSplit) > 1 and lSplit[1].lower() in ["kapitel"]):
            # print("[DELETED:", line, "]")
            new_chapter_title = line.strip()
            chapters.append([new_chapter_title, []])
        else:
            chapters[-1][-1].append(line)
            # print(line)
        # if "one" in line.lower():
        #     breakpoint()
    i = 0

    # Filter chapters
    new_chapters = []
    for chapter in chapters:
        non_blank = [c for c in chapter[1] if c.strip() != ""]
        if len(non_blank) <= 3:
            continue


        # Find % of lines within a % of max line length
        # Idea is to move chapters which don't use the full width as they're likely intro/contents stuff
        count = 0
        for line in chapter[1]:
            if len(line) > 0.8 * max_line_length:
                count += 1
        percentage_longer = count / len(chapter[1])
        if percentage_longer < 0.5:
            continue

        # If all good, append
        new_chapters.append(chapter)

    # breakpoint()
    chapters = new_chapters

    if len(new_chapters) == 0:
        return


    with open("output/"+num_id+".txt", 'w') as f:
        i = 0
        for chapter in chapters:
            print()
            print("Chapter", i)
            f.write("[SECTION]\n")
            i += 1
            for line in chapter[1]:
                print(line.encode("ascii", "xmlcharrefreplace"))
                f.write(line + "\n")
            print()

        # Add license back in
        with open("gutenberg_license.txt") as f_license:
            for line in f_license:
                f.write(line)
            # print("...")

        # print("|"+line+"|")
    # import sys;sys.exit()

    # first_chapter_indicators = ["chapter", "part", "chapitre"]
    # for indicator in first_chapter_indicators:
    #     if indicator +" 1" in book.lower() or indicator +" i" in book.lower():
    #         print("Chapter")
    #         breakpoint()



if __name__ == "__main__":
    # while True:
    get_text(1115)#input("bookId: "))
    import sys;sys.exit()

    done_english_ids = []

    import json
    with open("book_pairs.json") as f:
        for line in f:
            line = json.loads(line)
            print(line["english_book"]["title"])
            if line["english_book"]["id"] not in done_english_ids:
                get_text(line["english_book"]["id"])
                done_english_ids.append(line["english_book"]["id"])
            print(line["translated_book"]["language"])
            get_text(line["translated_book"]["id"], line["translated_book"]["language"])

