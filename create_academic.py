import argparse
import os

#-- command line parameters
#-- Read the system arguments listed after the program
parser = argparse.ArgumentParser(
    description="""Read a bibtex file to create website architecture for Hugo website
        """
)
parser.add_argument("--file","-f",
    help="bibtex file")
#-- working data directory
parser.add_argument("--directory","-D",
    help="Website directory for creating the file arborescence")
#-- output file
parser.add_argument("--overwrite","-O",
    default=False, action="store_true",
    help="Overwrite existing files")
args,_ = parser.parse_known_args()

listtoread = ["title", "year", "month", "author", "booktitle", "journal", "volume", "pages", "url", "abstract", "note"]

with open(args.file, "r") as file:
    full_text = file.read()
    articles = full_text.split("\n\n")

    for article in articles:
        lines = article.split("\n")
        folder_name = lines[0].split("{")[1][:-1]

        dic = {}
        for info in listtoread:
            dic[info] = ""
        if "inproceedings" in lines[0]:
            dic["publication_types"] = "1"
        else:
            dic["publication_types"] = "2"

        for info in listtoread:
            for line in lines:
                if info in line.split("=")[0]:
                    dic[info] = line.split("{")[1][:-2]
                    break


        dic["date"] = dic["year"] + "-" + dic["month"] + "-01"
        list_author = [i.split(', ') for i in dic["author"].split(' and ')]
        for i in range(len(list_author)):
            if '-' in list_author[i][1]:
                prenom = list_author[i][1].split('-')
                list_author[i][1] = prenom[0][0] + ".-" + prenom[1][0] + "."
            else:
                list_author[i][1] = list_author[i][1][0] + "."
        list_author = [i[0] + ', ' + i[1]  for i in list_author]
        list_author[list_author.index("Lecomte, H.")] = '**' + list_author[list_author.index("Lecomte, H.")] + '**'
        dic["authors"] = ', '.join(list_author[:-1]) + ' and ' + list_author[-1]
        if dic["journal"]:
            dic["booktitle"] = dic["journal"]

        if dic["volume"] and dic["pages"]:
            dic["info"] = ', ' + dic["volume"] + ', ' + dic["pages"]
        elif dic["volume"]:
            dic["info"] = ', ' + dic["volume"]
        elif dic["pages"]:
            dic["info"] = ', ' + dic["pages"]
        else:
            dic["info"] = ''

        if not(os.path.isdir(os.path.join("content", args.directory, folder_name))):
            os.mkdir(os.path.join("content", args.directory, folder_name))

        if args.overwrite or not(os.path.isfile(os.path.join("content", args.directory, "index.md"))):
            text = '---\n'
            text += 'title: "' + dic["title"] + '"\n'
            text += 'date: ' + dic["date"] + '\n'
            text += 'authors: "' + dic["authors"] + '"\n'
            text += 'publication_types: "' + dic["publication_types"] + '"\n'
            text += 'abstract: "' + dic["abstract"] + '"\n'
            text += 'publication: "' + dic["booktitle"] + '"\n'
            text += 'info: "' + dic["info"] + '"\n'
            text += 'doi: "' + dic["url"] + '"\n'
            text += 'note: "' + dic["note"] + '"\n'
            text += '---'

            with open(os.path.join("content", args.directory, folder_name, "index.md"), "w") as file:
                file.write(text)
