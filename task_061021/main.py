import re
with open('book.txt', encoding='utf-8') as book:
	lines = book.read()
	# lines = [line.strip() for line in book if "Chapter 1" in line]
	# for line in lines:
	# 	if line.strip() == "Chapter 1":
	# 		var = []
	# 		var.append(line.strip())

	results = re.search("Chapter 59", lines)

	# print(lines)
	print(results)
