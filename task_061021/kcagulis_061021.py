# Author - Kristiāns Francis Cagulis
# Date - 06.10.2021
import re

CHAPTERS = 61


# creates file with chapters and row numbers
def read_array(document):
	with open(document, encoding='utf-8') as book:
		lines = [line.strip('\n') for line in book]  # removes 'enter' characters
	with open('array_output.txt', 'w') as output:
		for i in range(1, CHAPTERS + 1):
			line = lines.index(f"Chapter {i}") + 1  # finds all chapter indexes/lines
			output.write(f"Line {line} - Chapter {i}\n")  # writes line in file


# creates file with chapter positions
def read_string(document):
	with open(document, encoding='utf-8') as book:
		lines = book.read()
	with open('str_output.txt', 'w') as output:
		for i in range(1, CHAPTERS + 1):
			_, position = re.finditer(rf"\bChapter {i}\b", lines)  # finds all chapter positions
			output.write(f"Position {position.start()} - Chapter {i}\n")  # writes position in file


def read_book(document):
	read_array(document)
	read_string(document)


def main():
	try:
		document = "book.txt"
		read_book(document)
	except:
		try:
			document = "1342-0.txt"
			read_book(document)
		except:
			document = input("Ievadiet faila nosaukumu: ")
			read_book(document)


if __name__ == '__main__':
	main()