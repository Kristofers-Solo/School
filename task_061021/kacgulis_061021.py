# Author - Kristiāns Francis Cagulis
# Date - 06.10.2021

CHAPTERS = 61


def read_array():
	with open('book.txt', encoding='utf-8') as book:
		lines = [line.strip('\n') for line in book]  # removes 'enter' characters
		with open('array_output.txt', 'w') as output:
			for i in range(1, CHAPTERS + 1):
				line = lines.index(f"Chapter {i}") + 1  # finds all chapter indexes/lines
				output.write(f"Line {line} - Chapter {i}\n")  # writes line in file


def read_string():
	import re
	with open('book.txt', encoding='utf-8') as book:
		lines = book.read()
		with open('str_output.txt', 'w') as output:
			for i in range(1, CHAPTERS + 1):
				_, position = re.finditer(rf"\bChapter {i}\b", lines)  # finds all chapter positions
				output.write(f"Position {position.start()} - Chapter {i}\n")  # writes position in file


def main():
	read_array()
	read_string()


if __name__ == '__main__':
	main()