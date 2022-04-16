import csv
import operator
from os.path import join, exists

fields = ["Name", "Score"]


def write_score(name: str, score: int, base_path: str) -> None:
	create_header = False
	path = join(base_path, "score.csv")
	if not exists(path):
		create_header = True
	with open(path, 'a', encoding='UTF-8', newline='') as file:
		write = csv.writer(file)
		if create_header:
			write.writerow(fields)
		write.writerows([[name, score]])


def read_score(path: str):
	lines = []
	path = join(path, "score.csv")
	with open(path, 'r', encoding='UTF-8') as file:
		for line in csv.reader(file):
			lines.append(line)
		return lines


def sort(data, reverse: bool = False):
	data = sorted(data, key=operator.itemgetter(1), reverse=reverse)
	return data